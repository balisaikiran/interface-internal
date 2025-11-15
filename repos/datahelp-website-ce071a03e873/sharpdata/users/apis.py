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
    "getCred": f"frontend-{env_name}-getCredentials",
    "createCred": f"frontend-{env_name}-createCredentials",
    "deleteCred": f"frontend-{env_name}-userOffBoarding",
    "updateSett": f"frontend-{env_name}-updateSettings",
    "getSett": f"frontend-{env_name}-getSettings",
    "updateUserDetails": f"frontend-{env_name}-updateUserDetails",
    "userDetails": f"frontend-{env_name}-userDetails",
    "heatmap": f"frontend-{env_name}-checkHeatmapImage",
    "list_users": f"frontend-{env_name}-getFubUsers",
    "updateUser": f"frontend-{env_name}-updateUser",
    "update_user": f"frontend-{env_name}-updateFubUser",
    "add_user": f"frontend-{env_name}-addFubUser",
    "form_links": f"frontend-{env_name}-getFormLinks",
    "remove_user": f"frontend-{env_name}-removeFubUser",
    "fubWebhooks": f"frontend-{env_name}-fubWebhooks",
    "createCustomActivity": f"sisu-fub-{env_name}-createCustomSisuActivity",
    "sisu_custom_fields": f"frontend-{env_name}-customFieldsSisu",
    "transferPropertyFields": f"frontend-{env_name}-transferPropertyFields",
    "twilioFubWebhooks": f"frontend-{env_name}-twilioFubWebhooks",
    "customFieldMapping": f"frontend-{env_name}-customFieldMapping",
    "getWufooFormFields": f"frontend-{env_name}-getWufooFormFields",
    "getSisuFields": f"frontend-{env_name}-getSisuFields",
    "getOtcFields": f"frontend-{env_name}-getOtcFields",
    "autoPopulateTagsForTagIntegration": f"frontend-{env_name}-populateTagsForTagInt",
    "getFubDomain": f"frontend-{env_name}-getFubDomain",
    "TestAction": f"workflow-{env_name}-actionTester",
}
