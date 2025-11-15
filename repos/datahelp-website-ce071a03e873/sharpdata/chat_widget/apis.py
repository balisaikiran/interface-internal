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
    "chatAPI": f"chat-gpt-{env_name}-ChatAPI",
    "getChats": f"chat-gpt-{env_name}-getChats",
    "getConversations": f"chat-gpt-{env_name}-getConversations",
    "fubUsers": f"frontend-{env_name}-getFubUsers",
}
