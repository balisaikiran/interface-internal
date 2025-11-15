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


# if STAGE == "prod":
#     base_url = "https://lewatij9kj.execute-api.us-west-2.amazonaws.com"
# elif STAGE == "test":
#     base_url = "https://3vrfd0zlta.execute-api.us-west-2.amazonaws.com"
# else:
#     base_url = "https://wiqog2w5m8.execute-api.us-west-2.amazonaws.com"
#

api = {
    "list_templates": f"frontend-{env_name}-listTextTemplate",
    "create_template": f"frontend-{env_name}-createTextTemplate",
    "delete_template": f"frontend-{env_name}-deleteTextTemplate",
    "update_template": f"frontend-{env_name}-updateTextTemplate",
    "get_template": f"frontend-{env_name}-getTextTemplate",
}
