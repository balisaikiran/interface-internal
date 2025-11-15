import hmac
import hashlib
# from login.helper import make_api_call
from common_form import apis
import json
from sharpdata.helper import make_lambda_call


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
    lambda_name = apis.api.get('fubUsers')
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
    if not is_create:
        pl['fub_deal_id'] = fub_deal_id
        # pl['opp_key'] = opp_key
    lambda_name = apis.api.get('getFormLinks')
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
