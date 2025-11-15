from django.shortcuts import render
from django.http import HttpResponse
import json
from chat_widget import helper
import base64
from django.views.decorators.csrf import csrf_exempt


def decode_context(context_data):
    if len(context_data) > 0:
        try:
            if context_data[0][:-2] != "==":
                context_data_decoded = base64.b64decode(context_data[0] + "==")
            else:
                context_data_decoded = base64.b64decode(context_data[0])
            context_data_decoded = json.loads(context_data_decoded)
        except Exception:
            print("DECODE EXCEPTION:", Exception)
            return {"ERROR": True}
    return context_data_decoded


def extract_context_data(context_data_decoded):
    print(context_data_decoded)
    fub_person_id = context_data_decoded["person"]["id"]
    domain = context_data_decoded["account"]["domain"]
    person_resp = helper.get_fub_user(domain)
    team_id = person_resp.get("team_id")
    user_name = context_data_decoded["user"]["name"]

    return team_id, fub_person_id, domain, user_name


def list_conversations(request):
    context = {}
    input_data = dict(request.GET)
    context_data = input_data.get("context", [])
    signature = input_data.get("signature")

    context_data_decoded = decode_context(context_data)

    if "ERROR" in context_data_decoded.keys():
        HttpResponse("Something Went Wrong!!")

    context["context_data"] = context_data[0]
    context["signature"] = signature[0]
    team_id, fub_person_id, domain, user_name = extract_context_data(context_data_decoded)

    resp = helper.get_conversations(team_id, fub_person_id)
    print("get_conversations", resp)
    context["conversations_list"] = resp
    if len(resp) > 0:
        return render(request, "chat_widget/cb_list_conversations.html", context=context)
    else:
        return render(request, "chat_widget/cb_landing_page.html", context=context)


def get_previous_chats(request):
    print("REQUEST:", request)
    if request.method == "POST":
        pl = request.POST.dict()
        print("RECEIVED PAYLAOD:", pl)
        # Expected Formatx
        conversation_id = pl['conversation_id']
        last_evaluated_key = {"conversation_id": pl['last_evaluated_key[conversation_id]'], "timestamp": pl['last_evaluated_key[timestamp]']}
        print("pl", conversation_id, last_evaluated_key)
        resp = helper.get_chats(conversation_id, last_evaluated_key)
        print("resp", resp)
        response = {}
        response["statusCode"] = 200
        response["message_response"] = resp["message_data"]
        response["last_evaluated_key"] = resp["last_evaluated_key"]
        return HttpResponse(json.dumps(response))


@csrf_exempt
def send_message(request):
    print("in send message", request.POST)
    pl = {k: v[0] for k, v in dict(request.POST).items()}
    print("Payload:", pl)
    resp = helper.chat_api(pl)
    print(resp)
    response = {}
    response["statusCode"] = 200
    response["message_response"] = resp["message_response"]
    response["conversation_id"] = resp["conversation_id"]
    return HttpResponse(json.dumps(response))


def chat(request):
    context = {}

    input_data = dict(request.GET)
    context_data = input_data.get("context", [])
    signature = input_data.get("signature")
    conversation_id = input_data.get("conversation_id")

    context_data_decoded = decode_context(context_data)

    if "ERROR" in context_data_decoded.keys():
        HttpResponse("Something Went Wrong!!")

    team_id, fub_person_id, domain, user_name = extract_context_data(context_data_decoded)
    context["team_id"] = team_id
    context["fub_person_id"] = fub_person_id
    context["user_name"] = user_name
    if domain:
        context["platform"] = "FUB"

    context["context_data"] = context_data[0]
    context["signature"] = signature[0]

    if conversation_id:
        print("ADDED conversation ID:", conversation_id)
        context["conversation_id"] = conversation_id[0]

        # Unhash for previous chat data
        conversation_data = helper.get_chats(conversation_id[0], None)
        print(type(conversation_data), conversation_data, conversation_data['message_data'])
        previous_chats = conversation_data['message_data']
        previous_chats.reverse()
        print("PREVIOUS CHATS:", previous_chats)
        # context["previous_chats"] = previous_chats
        context['last_evaluated_key'] = conversation_data['last_evaluated_key']

        # Remove when testing for previous chat data
        context['previous_chats'] = conversation_data

    context["context_data"] = context_data[0]
    context["signature"] = signature[0]
    print("CHAT BOT CONTEXT ON LOAD:", context)
    return render(request, "chat_widget/cb_chat.html", context=context)
