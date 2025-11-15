import requests
import json
fub_header = {'content-type': 'application/json', 'Accept': 'text/plain', 'X-System': 'Interface',  # 'datahelp-platform', 
                        'X-System-Key': 'b0c557612c52720182b4fd0b4051685c'}
import uuid

def get_secret(secret_name, SECRETS_NAMESPACE):
    import os
    import boto3
    from botocore.exceptions import ClientError

    secretsNamespace = SECRETS_NAMESPACE
    secretsRegion = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=secretsRegion)
    try:
        # SecretId is a combination of the secret's namespace and the specific secret to return
        print("Fetching Secret:", secretsNamespace + secret_name)
        response = client.get_secret_value(SecretId=secretsNamespace + secret_name)
    except ClientError as e:
        # Handle specific errors
        print(e)
        raise e
    else:
        apiKey = response["SecretString"]
    return apiKey


class Keys():
    # Private variables expected to be access by class name i.e. 'Keys'
    __team = ""
    # Team Keys
    __team_keys = {}
    # Hubspot header
    __hubspot_headers = {}
    # wufoo_key
    __wufoo_key = ""
    # twilio keys/id
    __twilio_sid = ""
    __twilio_key = ""
    # This is self managed class, hence no setters are present so that the keys are not overwritten by mistake

    def __init__(self, team="", market="real_estate") -> None:
        self.market = market
        self.team = team

    def _team_keys(self) -> dict:
        if self.team:
            # Check if the team name was changed, not really necessary, but kept just in case
            if self.team == Keys.__team and Keys.__team_keys:
                return Keys.__team_keys
            else:
                print("new team or tema keys not fetched")
                Keys.__team_keys = json.loads(get_secret(self.team))
                Keys.__team = self.team
                return Keys.__team_keys
        else:
            # send_slack_notification("general-notification", "Team Name Not Set")
            print("Team name not set, No keys found")
            return {}

    @property
    def fub_key(self) -> str:
        # No market check added as of now
        # if self.market:
        return self._team_keys().get("fub_key", "")

    @property
    def fub_key_name(self) -> str:
        return "fub_key" + "_" + self.team

    @property
    def otc_key(self) -> str:
        # No market check added as of now
        # if self.market:
        return self._team_keys().get("otc_key", "")

    @property
    def sisu_key(self) -> str:
        if self.market:
            return self._team_keys().get(f"sisu_{self.market}_key")
        else:
            print("Market not set, returning realestate keys")
            # send_slack_notification("general-notification", "Market Name Not Set")
            return self._team_keys().get(f"sisu_real_estate_key")

def data_type_url(data_type):
    urls = {
        "people": "https://api.followupboss.com/v1/people",
        "notes": "https://api.followupboss.com/v1/notes",
        "pipelines": "https://api.followupboss.com/v1/pipelines",
        "deals": "https://api.followupboss.com/v1/deals",
        "users": "https://api.followupboss.com/v1/users",
        "calls": "https://api.followupboss.com/v1/calls",
        "tasks": "https://api.followupboss.com/v1/tasks",
        "webhooks": "https://api.followupboss.com/v1/webhooks",
        "textMessages": "https://api.followupboss.com/v1/textMessages",
        "emails": "https://api.followupboss.com/v1/emails",
        "appointments": "https://api.followupboss.com/v1/appointments",
        "actionPlansPeople": "https://api.followupboss.com/v1/actionPlansPeople",
        "smartLists": "https://api.followupboss.com/v1/smartLists",
        "peopleRelationships": "https://api.followupboss.com/v1/peopleRelationships"
    }
    url = urls.get(data_type)
    return url


def post_data(fub_key, payload, data_type, params={}):
    import requests
    import json
    url = data_type_url(data_type)
    try:
        response = requests.post(
            url,
            auth=(fub_key, "pass"),
            data=json.dumps(payload),
            headers=fub_header,
            params=params,
        )
        print(response)
        print(response.content)
    except Exception as e:
        print(e)
        response = e

    return response


def put_webhook(fub_key, payload, webhook_id):
    import requests
    import json
    url = 'https://api.followupboss.com/v1/webhooks/' + webhook_id
    try:
        response = requests.put(url, auth=(fub_key, 'pass'), data=json.dumps(payload), headers=fub_header)
        print(response)
        print(response.content)
    except Exception as e:
        print(e)
        response = e
    return response


def get_webhook(fub_key):
    payload = {
        "limit": "100"
    }
    try:
        response = requests.get('https://api.followupboss.com/v1/webhooks', auth=(fub_key, 'pass'), params=payload, headers=fub_header)
        print(response)
        print(response.content)
    except Exception as e:
        print(e)
        response = e
    return response

def get_data(fub_key, payload, data_type, url=None):
    import requests
    import json
    import time

    print("get_data: ", fub_key, payload, data_type)
    return_meta_data = False
    if url:
        return_meta_data = True
    else:
        url = data_type_url(data_type)
    try:
        response = requests.get(
            url, auth=(fub_key, "pass"), params=payload, headers=fub_header
        )
        print(response)
        while response.status_code == 429:
            print("RATE LIMIT ERROR: Sleep for a sec", response)
            time.sleep(1)
            response = requests.get(
                url, auth=(fub_key, "pass"), params=payload, headers=fub_header
            )
        data = json.loads(response.text)
        if return_meta_data is False:
            data = data.get(data_type)
        print("data: ", data, response.content)
    except Exception as e:
        print(e)
        data = False
    return data


def get_data_by_id(fub_key, Id, data_type, payload={}):
    import requests
    import json

    url = data_type_url(data_type) + "/" + Id
    try:
        response = requests.get(
            url, auth=(fub_key, "pass"), params=payload, headers=fub_header
        )
        print(response)
        data = json.loads(response.text)
    except Exception as e:
        print(e)
        data = e

    return data

def put_data_by_id(fub_key, Id, data_type, payload={}):
    import requests
    import json

    print(data_type, data_type_url(data_type), Id)
    url = data_type_url(data_type) + "/" + Id
    try:
        response = requests.put(
            url, auth=(fub_key, "pass"), data=json.dumps(payload), headers=fub_header
        )
        print(response)
        data = json.loads(response.text)
        print(data)
    except Exception as e:
        print(e)
        data = e

    return data


def get_all_webhooks():
    get_webhook_response = get_webhook(fub_key)
    webhooks = json.loads(get_webhook_response.text).get("webhooks")
    return webhooks


def create_all_webhooks():
    for webhook_type in types:
        if webhook_type in hashs[env]:
            hash_value = hashs[env][webhook_type]
        else:
            hash_value = hashs[env]['default']
        route = routes.get(webhook_type, webhook_type)
        if market:
            prod_api_endpoint = (
                f"https://{hash_value}.execute-api.us-west-2.amazonaws.com/{route}?team={team}&market={market}"
            )
        else:
            prod_api_endpoint = (
                f"https://{hash_value}.execute-api.us-west-2.amazonaws.com/{route}?team={team}"
            )
        create_payload = {"event": webhook_type, "url": prod_api_endpoint}
        post_data(fub_key, create_payload, "webhooks")


def activate_env_webhooks():
    put_payload = {
            "status": "Active",
            }       
    for webhook in get_all_webhooks():
        if any(map(lambda x: x in webhook['url'], hashs[env].values())):
            _ = put_data_by_id(fub_key, str(webhook['id']), 'webhooks', payload=put_payload)


def delete_all():
    url = "https://api.followupboss.com/v1/webhooks/"
    headers = {"Accept": "application/json"}
    for webhook in get_all_webhooks():
        response = requests.request("DELETE", url + str(webhook['id']), headers=fub_header, auth=(fub_key, "pass"),)
        print(response)

def delete_ids(ids):
    url = "https://api.followupboss.com/v1/webhooks/"
    headers = {"Accept": "application/json"}
    for webhook in ids:
        response = requests.request("DELETE", url + str(webhook), headers=fub_header, auth=(fub_key, "pass"),)
        print(response)


def disable_all():
    put_payload = {
        "status": "Disabled",
        }
    for i in get_all_webhooks():
        _ = put_data_by_id(fub_key, str(i['id']), 'webhooks', payload=put_payload)


def update_webhooks():
    for i in get_all_webhooks():
        if i['event'] in types:
            params = extra_params.get(i['event'], {})
            webhook_type = i['event']
            if webhook_type in hashs[env]:
                hash_value = hashs[env][webhook_type]
            else:
                hash_value = hashs[env]['default']
            route = routes.get(webhook_type, webhook_type)
            if market:
                prod_api_endpoint = (
                    f"https://{hash_value}.execute-api.us-west-2.amazonaws.com/{route}?team={team}&market={market}"
                )
            else:
                prod_api_endpoint = (
                    f"https://{hash_value}.execute-api.us-west-2.amazonaws.com/{route}?team={team}"
                )
            for key, value in params.items():
                prod_api_endpoint = prod_api_endpoint + f"&{key}={value}"
            put_payload = {"url": prod_api_endpoint}
            _ = put_data_by_id(fub_key, str(i['id']), 'webhooks', payload=put_payload)
        else:
            print(f"!! Some thing is wrong, Create webhook first with name {i['event']} !!")


def update_webhooks_by_type(webhook_type):
    for i in get_all_webhooks():
        if i['event'] == webhook_type:
            params = extra_params.get(i['event'], {})
            webhook_type = i['event']
            if webhook_type in hashs[env]:
                hash_value = hashs[env][webhook_type]
            else:
                hash_value = hashs[env]['default']
            route = routes.get(webhook_type, webhook_type)
            if market:
                prod_api_endpoint = (
                    f"https://{hash_value}.execute-api.us-west-2.amazonaws.com/{route}?team={team}&market={market}"
                )
            else:
                prod_api_endpoint = (
                    f"https://{hash_value}.execute-api.us-west-2.amazonaws.com/{route}?team={team}"
                )
            for key, value in params.items():
                prod_api_endpoint = prod_api_endpoint + f"&{key}={value}"
            put_payload = {"url": prod_api_endpoint}
            _ = put_data_by_id(fub_key, str(i['id']), 'webhooks', payload=put_payload)
        else:
            print(f"pass {i['event']} !!")


def create_one_webhook(webhook_type):
    if webhook_type in hashs[env]:
        hash_value = hashs[env][webhook_type]
    else:
        hash_value = hashs[env]['default']
    route = routes.get(webhook_type, webhook_type)
    if market:
        prod_api_endpoint = (
            f"https://{hash_value}.execute-api.us-west-2.amazonaws.com/{route}?team={team}&market={market}"
        )
    else:
        prod_api_endpoint = (
            f"https://{hash_value}.execute-api.us-west-2.amazonaws.com/{route}?team={team}"
        )
    params = extra_params.get(webhook_type, {})
    for key, value in params.items():
        prod_api_endpoint = prod_api_endpoint + f"&{key}={value}"
    create_payload = {"event": webhook_type, "url": prod_api_endpoint}
    post_data(fub_key, create_payload, "webhooks")


def create_list_webhooks(webhook_types):
    for webhook_type in webhook_types:
        create_one_webhook(webhook_type)


routes = {"dealsUpdated": "fubTwoWaySync", "dealsCreated": "fubTwoWaySync",  "notesCreated": "NoteCreatedEndpoint"}
hashs = {'Dev':{'default': '2kq39uaoc6',"peopleTagsCreated": "lpy2v15aye", "dealsCreated": "lpy2v15aye", "dealsUpdated": "lpy2v15aye", "notesCreated": "lpy2v15aye"},
                'Test':{'default': '3hn3lnp5vi', "peopleTagsCreated":"yo1kwurnqg", "dealsUpdated": "yo1kwurnqg", "notesCreated": "yo1kwurnqg"},
                'Prod': {'default':'lk2696yw93', "peopleTagsCreated":"m0yy8xhnrf", "dealsUpdated": "m0yy8xhnrf", "dealsCreated": "m0yy8xhnrf","notesCreated": "m0yy8xhnrf"}
            }
types = ['callsCreated', 'emailsCreated', 'peopleCreated', 
                    'textMessagesCreated', 'peopleTagsCreated', 'dealsUpdated', 'notesCreated', 'dealsCreated']
extra_params = {
    # 'textMessagesCreated': {'trigger_id': 'JTG-FubTextCreated'},
    # 'dealsUpdated': {'trigger_id': 'DataHelp-FubDealUpdate',
    #                 },
    # "emailsCreated": {"trigger_id": "serrihometeam-FubEmailCreated"},
    # "notesCreated": {"trigger_id": "serrihometeam-FubNoteCreated"},
    # "textMessagesCreated": {"trigger_id": "serrihometeam-FubTextCreated"},
    # 'callsCreated': {"trigger_id": "f2fdb8ad33f84717b1b02e91ca0765ea"},
}
print("Note Extra Params:", extra_params)
team = "JCRE"

print("Team :", team)
assert team, "Team is a must"
market = ""  # recruiting, mortgage, ''
if market == "real_estate":
    market = ''
assert market in ["recruiting", "mortgage", ""]
env = 'Prod'
print("Env:", env)
assert env in ['Dev', 'Test', 'Prod']
SECRETS_NAMESPACE = '/' + env + '-' + 'env/'
fub_key = json.loads(get_secret(team, SECRETS_NAMESPACE)).get('fub_key')
# fub_key = ''
assert fub_key, "FUB Key Not Found"
# print(fub_key)
# fub_key = 'fka_0fI9zh3SfEPH37ssrSWTi54K17sUJduNM8'
# delete_all()
# team = 'test3'
# delete_ids([167])
# create_list_webhooks(['notesCreated', 'emailsCreated', 'textMessagesCreated', 'callsCreated'])
# create_list_webhooks(['dealsUpdated'])
# update_webhooks_by_type('dealsUpdated')

# update_webhooks_by_type('dealsUpdated')
######################################
## Push embeddapp users in table
# import boto3
# from boto3.dynamodb.conditions import Key
# url = "https://api.followupboss.com/v1/users"
# limit_per_request = 100
# payload = {"limit": limit_per_request, "offset": 0}
# fub_data_list = []
# completed = False
# table_name = "frontend-prod-env-FubEmbeddedAppUsers-DZ7MNE0VQEQT"
# dynamodb = boto3.resource("dynamodb")
# user_table = dynamodb.Table(table_name)

# user_data = user_table.query(
#         IndexName='team_id-index',
#         KeyConditionExpression=Key('team_id').eq(team)
# )
# while not completed:
#     fub_data = get_data(fub_key, payload, "users", url)
#     print("got data", fub_data)
#     fub_data_list.extend(fub_data.get("users"))
#     if len(fub_data.get("users")) < limit_per_request:
#         completed = True
#     else:
#         url = fub_data.get("_metadata").get("nextLink")
# print('FUB data: ', fub_data_list)

# for d in fub_data_list:
#     osa = f"{d['firstName'] + ' ' + d['lastName']}" in ['Paul Burke']
#     isa = f"{d['firstName'] + ' ' + d['lastName']}" in []
#     admin = f"{d['firstName'] + ' ' + d['lastName']}" in []
#     if not osa:
#         continue
#     if not isa:
#         isa = None
#     else:
#         isa = "ISA"
#     if admin:
#         isa = "ADMIN"
#     print({
#             "fub_id": d['id'],
#             "email": d['email'],
#             "team_id": team,
#             "is_osa": osa,
#             "isa_or_admin": isa,
#             "name": f"{d['firstName'] + ' ' + d['lastName']}",
#             "userId": f"{team}_fub_{d['id']}"
#         })
#     print("---")
#     resp = user_table.put_item(
#         Item={
#             "fub_id": d['id'],
#             "email": d['email'],
#             "team_id": team,
#             "is_osa": osa,
#             "isa_or_admin": isa,
#             "name": f"{d['firstName'] + ' ' + d['lastName']}",
#             "userId": f"{team}_fub_{d['id']}"
#         }
#     )
#     print(resp)
# h
########################################
# market should be one of ['recruiting',' mortgage', ''] (don't put real_estate as string, put as empty str for real_estate)
assert market in ['recruiting', ' mortgage', '']


# old flow, it deleted and created webhooks
# fub_header = {'content-type': 'application/json', 'Accept': 'text/plain', 'X-System': 'datahelp-platform', 
#                         'X-System-Key': 'b0c557612c52720182b4fd0b4051685c'}
# delete_all()
# create_all_webhooks()
# disable_all()
# activate_env_webhooks()

# New flow, just edits the exsisting one
# update_webhooks()
# put_payload = {
#         "status": "Disabled",
#         }
# for id in [15, 17]:
#     put_data_by_id(fub_key, str(id), 'webhooks', payload=put_payload)
# delete_ids([246])
# create_payload = {"event": "peopleCreated", "url": f"https://lk2696yw93.execute-api.us-west-2.amazonaws.com/peopleCreated?team={team}&market=recruiting"}
# create_payload = {"event": "dealsUpdated", "url": f"https://{hashs[env]['dealsUpdated']}.execute-api.us-west-2.amazonaws.com/fubTwoWaySync?team={team}"}
# post_data(fub_key, create_payload, "webhooks")
# create_payload = {"event": "dealsCreated", "url": f"https://{hashs[env]['deal']}.execute-api.us-west-2.amazonaws.com/fubTwoWaySync?team={team}"}
# post_data(fub_key, create_payload, "webhooks")

# create_payload = {"event": "peopleTagsCreated", "url": "https://m0yy8xhnrf.execute-api.us-west-2.amazonaws.com/peopleTagsCreated?team=bringashometeam&market=recruiting"}
# post_data(fub_key, create_payload, "webhooks")
# response = requests.request("DELETE", "https://api.followupboss.com/v1/webhooks/" + str(197), headers=fub_header, auth=(fub_key, "pass"),)
# print(get_data(fub_key, {'personId': 7181}, "emails"))
# get_data_by_id(fub_key, "1", "emails")
webhooks = get_all_webhooks()
n = 0
for w in webhooks:
    n += 1
    print(w)
    print("---")
# print(webhooks)
print(n)

print("SISU URL", f'https://lk2696yw93.execute-api.us-west-2.amazonaws.com/sisuTwoWaySync?team={team}')