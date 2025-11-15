import json
import boto3

try:
    f = open("/var/www/config", "r")
    data = json.loads(f.read())
    f.close()
    STAGE = data.get('STAGE', 'dev')
except Exception as e:
    print(e)
    STAGE = "dev"

if STAGE == 'dev':
    dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
    table = dynamodb.Table('website-config')
    response = table.get_item(Key={'key': 'sandbox'})
    env_name = response['Item']['env_name']
elif STAGE == 'test':
    env_name = 'test-env'
else:
    env_name = 'prod-env'

api = {
    "listOpportunities": f"frontend-{env_name}-listOpportunities",
    "createOpportunityForm": f"frontend-{env_name}-createOpportunityForm",
    "getOpportunityForm": f"frontend-{env_name}-getOpportunityForm",
    "getOpportunityDetails": f"frontend-{env_name}-getOpportunityDetails",
    "updateOpportunityForm": f"frontend-{env_name}-updateOpportunityForm",
    "fubUsers": f"frontend-{env_name}-getFubUsers",
    "fubUsers_v2": f"frontend-{env_name}-getFubUsersV2",
    "getInterfaceFormLinks": f"frontend-{env_name}-getInterfaceFormLinks",
    "getFormLinks": f"frontend-{env_name}-getFormLinks",
    "oneClickEmbeddedApp": f"frontend-{env_name}-oneClickEmbeddedAppReceiver",
    "getFubPipelines": f"frontend-{env_name}-getFubPipelines",
}
