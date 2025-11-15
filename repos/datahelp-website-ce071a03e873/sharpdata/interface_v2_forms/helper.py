import hmac
import hashlib
# from login.helper import make_api_call
from interface_v2_forms import apis
import json
from sharpdata.helper import make_lambda_call
from graphqlclient import GraphQLClient


graphql_urls = {'local': 'http://localhost:4000/graphql', 'dev': 'https://api.sandbox.datalabz.re/graphql',
                'test': 'https://api.test.datalabz.re/graphql', 'prod': 'https://api.datalabz.re/graphql'}

form_builder_urls = {'local': 'http://localhost:3000/', 'dev': 'https://app.sandbox.datalabz.re/',
                     'test': 'https://app.test.datalabz.re/', 'prod': 'https://app.datalabz.re/'}


OpportunitiesByPersonId = '''
query OpportunitiesByPersonId($fubPersonId: String, $teamId: String) {
  opportunitiesByPersonId(fub_person_id: $fubPersonId, team_id: $teamId) {
    opp_key
    opp_updated_ts
    opp_stage
    opp_type
    fub_person_id
    opp_created_ts
    fub_deal_id
    teamFubDealId
    team
    sisu_client_id
    opp_isa
    opp_address
    appt_set_lead_type
    opp_address2
    opp_city
    opp_postal_code
    opp_last_name
    opp_state
    otc_property_id
    opp_price
  }
}
'''

FormNames = '''
query FormsNames($teamId: String) {
  formsNames(team_id: $teamId) {
    form_id
    form_name
  }
}
'''


def get_url(servername):
    URL = ""
    url_list = ""
    if servername == 'graphql':
        url_list = graphql_urls
    elif servername == 'embedded_app':
        url_list = form_builder_urls

    try:
        f = open("/var/www/config", "r")
        data = json.loads(f.read())
        f.close()
        STAGE = data.get('STAGE', 'dev')
    except Exception as e:
        print(e)
        STAGE = "local"

    if STAGE == 'local':
        URL = url_list.get('local')
    elif STAGE == 'dev':
        URL = url_list.get('dev')
    elif STAGE == 'test':
        URL = url_list.get('test')
    else:
        URL = url_list.get('prod')
    return URL


def getOpps(team_id, fub_person_id):
    endpoint = get_url('graphql')
    client = GraphQLClient(endpoint)
    resp = client.execute(OpportunitiesByPersonId, {"teamId": team_id, "fubPersonId": str(fub_person_id)})
    data = json.loads(resp)
    opp_data = data['data']['opportunitiesByPersonId']
    print(opp_data)
    return opp_data


def getForms(team_id):
    endpoint = get_url('graphql')
    client = GraphQLClient(endpoint)
    resp = client.execute(FormNames, {"teamId": team_id})
    # resp = client.execute(FormNames, {"teamId": "Ashwini_70"})
    data = json.loads(resp)
    forms = data['data']['formsNames']
    return forms, get_url('embedded_app')


def check_hash(context, signature, hash_key="2dcae62bb895dc30cbf2ac50eb595505"):
    if not hash_key:
        hash_key = "2dcae62bb895dc30cbf2ac50eb595505"
    digest = hmac.new(
        bytes(hash_key, 'UTF-8'),
        bytes(context[0], 'UTF-8'),
        hashlib.sha256)
    calculated_signature = digest.hexdigest()
    print("signature: ", signature[0])
    print("calculated_signature: ", calculated_signature)
    if signature[0] == calculated_signature:
        return True
    else:
        return False


def get_oppurtunity_list(domain, person):
    payload = {
        'domain': domain,
        'person': person
    }
    lambda_name = apis.api.get('listOpportunities')
    print(lambda_name)
    resp = make_lambda_call(lambda_name, payload, fetch_raw=True)
    # print(resp)
    if resp.get('statusCode', 404) != 200:
        return False, [], None, None
    elif 'body' in resp:
        opportunity_data = resp['body']['data']
        team_id = resp['body'].get('team_id')
        error = resp['body'].get('error')
    elif 'message' in resp:
        opportunity_data = []
        team_id = None
        error = None
    else:
        opportunity_data = []
        team_id = None
        error = None
    return True, opportunity_data, team_id, error


def get_oppurtunity_details(opp_key, team_id):
    pl = {
        'team_id': team_id,
        'opp_key': opp_key,
    }
    lambda_name = apis.api.get('getOpportunityDetails')
    print(lambda_name)
    resp = make_lambda_call(lambda_name, pl, fetch_raw=True)
    print(resp)
    if 'body' in resp:
        resp = resp['body']['data']
        if len(resp) > 0:
            resp = resp[0]
    return resp


def update_oppurtunity(pl):
    lambda_name = apis.api.get('createOpportunityForm')
    print(lambda_name)
    resp = make_lambda_call(lambda_name, pl, fetch_raw=True)
    print(resp)
    if 'body' in resp:
        resp = resp['body']['data']
    elif 'message' in resp:
        resp = []
    return resp


def get_fub_user(domain):
    pl = {
        'domain': domain
    }
    lambda_name = apis.api.get('fubUsers_v2')
    print(lambda_name)
    resp = make_lambda_call(lambda_name, pl, fetch_raw=True)
    # print(resp)
    return resp


def get_form_links(team_id, person_id, opp_key, is_create=True, fub_deal_id=None, ApptLinks=False):
    pl = {
        'team': team_id,
        "fub_person_id": str(person_id),
        "create_link": is_create,
        "ApptLinks": ApptLinks,
        "opp_key": opp_key
    }
    print("PLPL", pl)
    if not is_create:
        pl['fub_deal_id'] = fub_deal_id
        # pl['opp_key'] = opp_key
    lambda_name = apis.api.get('getInterfaceFormLinks')
    print(lambda_name)
    resp = make_lambda_call(lambda_name, pl, fetch_raw=True)
    print(resp)
    if 'body' in resp:
        resp = json.loads(resp['body'])
    return resp


def one_click_embedded_app(pl):
    lambda_name = apis.api.get('oneClickEmbeddedApp')
    print(lambda_name)
    resp = make_lambda_call(lambda_name, pl, fetch_raw=True)
    print(resp)
    if 'body' in resp:
        resp = resp['body']['data']
    elif 'message' in resp:
        resp = []
    return resp


def get_fub_pipelines(team_id):
    pl = {
        'team_id': team_id
    }
    lambda_name = apis.api.get('getFubPipelines')
    print(lambda_name)
    resp = make_lambda_call(lambda_name, pl, fetch_raw=True)
    print(".......", resp)
    if 'data' in resp:
        resp = resp['data']
    elif 'message' in resp:
        resp = []
    return resp
