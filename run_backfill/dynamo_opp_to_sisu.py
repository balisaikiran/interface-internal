import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
import json
import requests
import base64
import importlib

import psycopg2, psycopg2.extras
import os
import json
import decimal
import datetime
import requests
import random


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


def put_sisu_custom_fields(payload: "dict"):
    """
    :param payload:
    {
        "field_name": "{{custom_client_field_name}}",
        "field_type": "{{custom_client_field_type}}",
        "field_length": {{custom_client_field_length}},
        "tooltip": "Sample tooltip"
    }
    :return:
    """
    body = payload
    method_url = method_type("custom-field", team_id=team_id)
    try:
        response = requests.post(
            "{}{}".format(url, method_url),
            data=json.dumps(body),
            headers=headers,
            verify=True,
        )
        print(response, response.text)
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=False))
    except Exception as ex:
        print("Exception: {}".format(str(ex)))
    return json_response


def get_data(method_label: "str", Id: "str" = "") -> "dict":
    """API call function to get information from SISU according to method_label provided.
    Updates:
        method_url
        json_response
    Parameters:
        method_label (str): method type to get method url endpoint.
                            available labels: ["info", "get-team-agents", "activity",
                             "activity-types", "lead-expense", "agent-lead-counts"]
        Id (str): Agent ID to be updated.
    Returns:
        json_response (dict): Response for information update.
    """
    body = {}
    method_url = method_type(method_label)
    method_url = method_url + Id
    try:
        print("{}{}".format(url, method_url), "body", body, "headers", headers)
        response = requests.get(
            "{}{}".format(url, method_url),
            data=body,
            headers=headers,
            verify=True,
        )
        print(response)
        json_response = response.json()
        # print("json_response: ", json_response)
        # print(json.dumps(json_response, indent=4, sort_keys=False))
    except Exception as ex:
        json_response = None
        print("Exception: {}".format(str(ex)))
    return json_response


def method_type(
    method_label: "str",
    team_id: "str" = "",
    agent_id: "str" = "",
    reason_id: "str" = "0",
    client_id: "str" = "",
    client_stage_id: "str" = "",
):
    """Gives the URL endpoint for SISU according to the method type provided.
    Updates:
        method_url
    Parameters:
        method_label (str): method type to get method url endpoint.
                            available labels: ["info", "get-team-agents", "activity",
                                "activity-types", "lead-expense", "agent-lead-counts"]
    Returns:
        None.
    """
    # print("\n <<>> SISU METHOD URL FETCHING <<>> \n")
    methods = {
        "info": "/api/v1/team/info",
        "get-team-agents": "/api/v1/team/get-team-agents/",
        "activity": "/api/v1/agent/activity/",
        "activity-types": "/api/v1/team/activity-types/",
        "get-lead-sources": "/api/v1/team/get-lead-sources/",
        "lead-expense": "/api/v1/team/lead-expense/",
        "agent-lead-counts": "/api/v1/team/agent-lead-counts/",
        "edit-client": "/api/v1/client/edit-client/",
        "find-client": "/api/v1/client/find-client",
        "find-edit-client": "/api/v1/client/find-edit-client",
        "list-client": "/api/v1/client/list",
        "archive": "/api/v1/client/archive/",
        "custom-field": f"/api/v1/team/{team_id}/custom/client/field",
        "add_activity": "/api/v1/parameter/activity-types",
        "document": "/api/v1/client/documents",
        "reasons": f"/api/v1/archive-reasons/{agent_id}",
        "lost_client": f"/api/v1/client/edit-client/{client_id}?agent_id={agent_id}&reason_id={reason_id}",
        "create_client_stages": f"/api/v1/client-stages",
        "edit_client_stages": f"/api/v1/client-stages/{client_stage_id}/{team_id}",
        # "get_client_stages": f"/api/v1/client-stages/{client_stage_id}/{team_id}",
        "get_client_stages": f"/api/v1/client-stages/stages/{team_id}",
        "get_vendor": f"/api/v1/team/vendor?team_id={team_id}",
    }
    method_url = methods.get(method_label)
    # print("URL USED: ", method_url)
    return method_url


def get_sisu_custom_fields(team_id, url):
    method_url = method_type("custom-field", team_id=team_id)
    try:
        response = requests.get(
            "{}{}".format(url, method_url),
            headers=headers,
            verify=True,
        )
        print(response)
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=False))
    except Exception as ex:
        print("Exception: {}".format(str(ex)))
    return json_response


def post_request(body: dict) -> dict:
    try:
        # print(body)
        response = requests.post(
            "{}{}".format(url, method_url),
            data=json.dumps(body),
            headers=headers,
            verify=True,
        )
        # print(response)
        json_response = response.json()
        # print(json.dumps(json_response, indent=4, sort_keys=False))
    except Exception as ex:
        print("Exception: {}".format(str(ex)))
        json_response = {"Result": "Post Request Failed"}
    return json_response


def put_request(body: dict) -> dict:
    try:
        response = requests.put(
            "{}{}".format(url, method_url),
            data=json.dumps(body),
            headers=headers,
            verify=True,
        )
        print(response)
        json_response = response.json()
        # print(json.dumps(json_response, indent=4, sort_keys=False))
    except Exception as ex:
        print("Exception: {}".format(str(ex)))
        json_response = {"Result": "Post Request Failed"}
    return json_response



def full_table_query(table, **kwargs) -> dict:
    num_max_items = kwargs.pop("num_max_items", -1)
    response = table.query(**kwargs)
    Items = response["Items"]
    LastEvaluatedKey = response.get("LastEvaluatedKey", None)
    if len(Items) >= num_max_items and num_max_items != -1:
        print("returned Max items, possiblity of more items in table")
    else:
        while LastEvaluatedKey:
            print("getting item ")
            kwargs['ExclusiveStartKey'] = LastEvaluatedKey
            response = table.query(**kwargs)
            Items.extend(response["Items"])
            LastEvaluatedKey = response.get("LastEvaluatedKey", None)
            if len(Items) >= num_max_items and num_max_items != -1:
                print("returned Max items, possiblity of more items in table")
                break
    return {"Items": Items, "LastEvaluatedKey": LastEvaluatedKey}


def get_opp_table_name(market):
    if market == "real_estate":
        table_name = "OPP_TABLE"
    elif market == "mortgage":
        table_name = "LENDER_OPP_TABLE"
    elif market == "recruiting":
        table_name = "RECRUITER_OPP_TABLE"
    return table_name


def query_opportunities(opp_type, filter_key, team_id, dynamodb=None, market='real_estate'):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")
    table_name = get_opp_table_name(market)
    table = dynamodb.Table(os.environ[table_name])
    print("query_opportunities: ", table)
    Items = full_table_query(table,
                IndexName='opp_type-appt_set_entry_id-index',
                KeyConditionExpression='opp_type = :opp_type AND appt_set_entry_id= :appt_set_entry_id',
                ExpressionAttributeValues={
                    ':opp_type':  opp_type,
                    ':appt_set_entry_id': filter_key,
                },num_max_items=-1)['Items']
    if len(Items) > 0:
        print(Items)
        print("------------------")
        for item in Items:
            if item.get('team') == team_id:
                return item
        return Items[0]
    return Items


def query_all_opportunities_team(team_id, dynamodb=None, market='real_estate', num_max_items=-1):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")
    table_name = get_opp_table_name(market)
    table = dynamodb.Table(os.environ[table_name])
    print("query_opportunities: ", table)
    Items = full_table_query(table,
                IndexName='team-index',
                KeyConditionExpression='team = :team',
                ExpressionAttributeValues={
                    ':team':  team_id,
                },num_max_items=num_max_items)['Items']
    return Items


def update_opportunityTable(table_key, opportunity_payload, market="real_estate", dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb")
    table_name = get_opp_table_name(market)
    print("table_name: ", table_name, market, table_key)
    table = dynamodb.Table(os.environ[table_name])
    response = "Not done"
    for attribute_names, attribute_values in opportunity_payload.items():
        if attribute_names == OPP_TABLE_PARTITION_KEY:
            continue
        response = table.update_item(
            Key={OPP_TABLE_PARTITION_KEY: table_key},
            UpdateExpression="set #attrName = :attrValue",
            ExpressionAttributeNames={"#attrName": attribute_names},
            ExpressionAttributeValues={":attrValue": attribute_values},
            ReturnValues="UPDATED_OLD",
        )
    print("update_opportunityTableresponse: ", response)
    return response


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        if isinstance(o, datetime.date):
            return str(o)
        return super(DecimalEncoder, self).default(o)


# sisu_username = "real-estate-data-help"
# sisu_key = "c80791bb-0627-4f9f-9211-6745c3ed3501"
market = "real_estate"
team = "whisselrealtygroup"

env = "Prod"
OPP_TABLE_PARTITION_KEY = "teamFubDealId"
assert env in ["Dev", "Test", "Prod"]
SECRETS_NAMESPACE = "/" + env + "-" + "env/"

# print(query_opportunities("Seller", "200", "Jenson"))
import time
start_time = time.time()
opps = query_all_opportunities_team(team, num_max_items=-1, market=market)
opps = json.loads(json.dumps(opps, cls=DecimalEncoder))
print(len(opps))
print("end_time: ", time.time() - start_time)
# dump opp_data to file
with open("opps.json", "w") as f:
    json.dump(opps, f)

# Open opps.json
with open("opps.json", "r") as f:
    opps = json.load(f)
i = 0

keys = json.loads(get_secret(team, SECRETS_NAMESPACE))
sisu_key = keys.get(f"sisu_{market}_key")
sisu_username = keys.get(f"sisu_{market}_username")

# print(sisu_key, sisu_username)
# sisu_username, sisu_key = "jeff-cook-real-estate,-llc---recruiting-&-onboarding-19695", "47b7890e-db1f-415f-b71f-2b7396c602c8"
print(sisu_key, sisu_username)

url = "https://api.sisu.co"
user_agent = "realestatedatahelp"
b = bytes("{}:{}".format(sisu_username, sisu_key), "utf-8")
authentication = str(base64.b64encode(b), "utf-8")
authorization = "Basic {}".format(authentication)
print(authorization)

headers = {
    "Content-Type": "application/json",
    "Authorization": authorization,
    "User-agent": user_agent,
}

print("leng",len(opps))
# Push to sisu
# for opp in opps:
#     sisu_client_id = opp.get('sisu_client_id')
#     print(opp)
#     stop
    # if sisu_client_id:
    #     method_url = method_type("edit-client")

    #     total_payload = {
    #                     'custom': {
    #                                "fub_id": opp.get("fub_person_id"),
    #                                 }
    #                                 }
    #     print(sisu_client_id)
    #     method_url = method_url + str(sisu_client_id)
    #     print("method_url: ", method_url)
    #     sisu_client_response = post_request(total_payload)
