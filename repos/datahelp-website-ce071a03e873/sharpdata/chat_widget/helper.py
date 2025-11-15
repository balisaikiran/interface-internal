from chat_widget import apis
from sharpdata.helper import make_lambda_call
import hmac
import hashlib


def api_call_helper(api_name, pl, fetch_raw=True):
    lambda_name = apis.api.get(api_name)
    print(lambda_name)
    resp = make_lambda_call(lambda_name, pl, fetch_raw)
    print(resp)
    if 'body' in resp:
        resp = resp['body']['data']
        if len(resp) > 0:
            resp = resp[0]
    return resp


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


def get_fub_user(domain):
    pl = {
        'domain': domain
    }
    return api_call_helper('fubUsers', pl, fetch_raw=True)


def get_chats(conversation_id, last_evaluated_key):
    pl = {"conversation_id": conversation_id,
          "last_evaluated_key": last_evaluated_key
          }
    return api_call_helper('getChats', pl, fetch_raw=True)


def get_conversations(team_id, fub_person_id):
    pl = {
        "fub_person_id": str(fub_person_id),
        "team_id": team_id
    }
    return api_call_helper('getConversations', pl, fetch_raw=True)


def chat_api(pl):
    return api_call_helper('chatAPI', pl, fetch_raw=True)
