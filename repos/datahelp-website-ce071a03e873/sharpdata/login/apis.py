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
    "register": f"frontend-{env_name}-registerUser",
    "details": f"frontend-{env_name}-userDetails",
    "verify": f"frontend-{env_name}-verifyUser",
    "get_teams": f"frontend-{env_name}-getTeamIds",
    "send_confirmation_code": f"frontend-{env_name}-sendConfirmationCode",
    "forgot_password": f"frontend-{env_name}-forgotPassword"
}
