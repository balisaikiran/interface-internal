import traceback

from django.shortcuts import render
import base64

from common_form import helper
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import date
import json

OPP_KEY = 'teamFubDealId'

try:
    f = open("/var/www/config", "r")
    data = json.loads(f.read())
    f.close()
    STAGE = data.get("STAGE", "dev")
except Exception as e:
    print(e)
    STAGE = "dev"


# Create your views here.
@csrf_exempt
def loader(request):
    return render(request, "common_form/loader.html")


@csrf_exempt
def success(request):
    context = {}
    input_data = dict(request.GET)
    context["context_data"] = input_data.get("context", [])[0]
    context["signature"] = input_data.get("signature")[0]
    context["is_closed"] = input_data.get("is_closed", [False])[0]
    return render(request, "common_form/success.html", context=context)


# Create your views here.
@csrf_exempt
def common_form(request):
    """
    This is the common form
    :param request:
    :return:
    """
    context = {}
    input_data = dict(request.GET)
    context_data = input_data.get("context", [])
    signature = input_data.get("signature")
    if len(context_data) > 0:
        try:
            if context_data[0][:-2] != "==":
                context_data_decoded = base64.b64decode(context_data[0] + "==")
            else:
                context_data_decoded = base64.b64decode(context_data[0])
            context_data_decoded = json.loads(context_data_decoded)
        except Exception:
            return HttpResponse("Something Went Wrong!!")
    domain = context_data_decoded["account"]["domain"]
    person_id = context_data_decoded["person"]["id"]
    context["fub_person_id"] = person_id
    context["context_data"] = context_data[0]
    context["signature"] = signature[0]
    person_resp = helper.get_fub_user(domain)
    team_id = person_resp.get("team_id")
    if request.method == "GET":
        opp_key = request.GET.get("opp_key")
        if opp_key:
            resp = helper.get_oppurtunity_details(opp_key, team_id)
            context.update(resp)

        # Get fub users
        context["user_data"] = person_resp["data"]
        context["is_update"] = 0
        context["osa_list"] = sorted(
            [i for i in person_resp["data"]
             if i["is_osa"] is True], key=lambda i: i["name"]) if person_resp["data"] else []
        context["isa_list"] = ",".join(sorted(
            [i.get("name") for i in person_resp["data"]
             if i.get("isa_or_admin", "") == "ISA" or i.get("is_isa", False) is True],
            key=lambda i: i) if person_resp["data"] else [])
    if request.method == "POST":
        pl = request.POST.dict()
        del pl["csrfmiddlewaretoken"]
        pl["fub_person_id"] = person_id
        pl["opp_request_type"] = "create new opportunity"
        pl["domain"] = domain
        pl["lead_type"] = request.POST.get("lead_type")
        pl["emb_appt_version"] = 2
        pl["created_on"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        print("Payload", pl)
        resp = helper.update_oppurtunity(pl)
        # print(resp)
        return HttpResponseRedirect(
            f"../common_form/success?success=1&context={context_data[0]}&signature={signature[0]}"
        )
    hash_key = person_resp.get("secret_key", None)
    status = helper.check_hash(context_data, signature, hash_key)
    if not status:
        return HttpResponse("Invalid Signature, Something went wrong!")
    return render(request, "common_form/common_form.html", context=context)


@csrf_exempt
def common_form_fields(request):
    """"
        Summary:
            Function common_form_fields used for sending fields to frontend,
            Arrange as per Transaction type.

        Parameters :
            isa_list (list): isa_list is sent from frontend using ajax call.
            Transaction Type Fields JSON:
            Transaction Name:{
                {"field": "used as class name in HTML",
                "label": "Used as Name/Label",
                "required": "true/false #Makes Field required",
                "type": "select/time/text/number/state",
                "data": "value of data in list",
                "condition": "Javascript can be passed here"},
            }

        Returns: Dict -> Json of Fields
    """
    isa_list = request.GET.get("isa_list", [])
    Fields = {
        "Appointment_Set": [
            {"field": "opp_type", "label": "Lead Type", "required": "true", "type": "select",
             "data": "Buyer,Seller,BuyerSeller", "condition": "onChange('.opp_type > select',\'change\',\
             '{\"Buyer\":{\"display\":false,\"classes\":[\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]},\
             \"Seller\":{\"display\":true,\"classes\":[\"opp_address\", \"opp_city\",\"opp_state\",\"opp_postal_code\"]},\
             \"BuyerSeller\":{\"display\":true,\"classes\":[\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]}}',\
             [\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]);"},
            {"field": "opp_isa", "label": "ISA", "required": "false",
             "type": "select", "data": isa_list, "condition": ""},
            {"field": "opp_appt_date", "label": "Appointment Date", "required": "true",
             "type": "date", "data": "", "condition": ""},
            {"field": "appt_time", "label": "Appointment Time", "required": "true",
             "type": "time", "data": "", "condition": ""},
            {"field": "opp_address", "label": "Address",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "true", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "true", "type": "text", "data": "", "condition": ""}],
        "Pipeline": [
            {"field": "opp_type", "label": "Lead Type", "required": "true", "type": "select",
             "data": "Buyer,Seller,BuyerSeller", "condition": "onChange('.opp_type > select',\'change\',\
             '{\"Buyer\":{\"display\":false,\"classes\":[\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]},\
             \"Seller\":{\"display\":true,\"classes\":[\"opp_address\", \"opp_city\",\"opp_state\",\"opp_postal_code\"]},\
             \"BuyerSeller\":{\"display\":true,\"classes\":[\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]}}',\
             [\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]);"},
            {"field": "opp_isa", "label": "ISA", "required": "false",
             "type": "select", "data": isa_list, "condition": ""},
            {"field": "opp_address", "label": "Address",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "true", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "true", "type": "text", "data": "", "condition": ""}],
        "Agreement_Signed": [
            {"field": "opp_type", "label": "Lead Type", "required": "true", "type": "select",
                "data": "Buyer,Seller", "condition": "onChange('.opp_type > select',\'change\',\
             '{\"Buyer\":{\"display\":false,\"classes\":[\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]},\
             \"Seller\":{\"display\":true,\"classes\":[\"opp_address\", \"opp_city\",\"opp_state\",\"opp_postal_code\"]}}',\
              [\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"])"},
            {"field": "opp_price", "label": "Price", "required": "false", "type": "number",
                "data": "", "condition": ""},
            {"field": "opp_commission_percent", "label": "Commission Percentage",
                "required": "false", "type": "number", "data": "", "condition": ""},
            {"field": "opp_agreement_signed_date", "label": "Agreement Signed Date",
                "required": "true", "type": "date", "data": "", "condition": ""},
            {"field": "opp_agreement_expiration_date", "label": "Agreement Expiration Date",
                "required": "true", "type": "date", "data": "", "condition": ""},
            {"field": "opp_forecasted_close_date", "label": "Forecasted Close Date",
                "required": "false", "type": "date", "data": "", "condition": ""},
            {"field": "opp_address", "label": "Address",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "true", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "true", "type": "text", "data": "", "condition": ""}
        ],
        "Pending": [
            {"field": "opp_type", "label": "Transaction Type", "required": "true",
             "type": "select", "data": "Buyer,Seller"},
            {"field": "opp_price", "label": "Price", "required": "false", "type": "number",
             "data": "", "condition": ""},
            {"field": "opp_commission_percent", "label": "Commission Percentage",
             "required": "false", "type": "number", "data": "", "condition": ""},
            {"field": "opp_address", "label": "Address",
             "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
             "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "true", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_under_contract_date", "label": "Under Contract Date",
             "required": "true", "type": "date", "data": "", "condition": ""},
            {"field": "opp_forecasted_close_date", "label": "Forecasted Close Date",
                "required": "false", "type": "date", "data": "", "condition": ""}],
        "Closed": [
            {"field": "opp_type", "label": "Transaction Type", "required": "true",
             "type": "select", "data": "Buyer,Seller"},
            {"field": "opp_price", "label": "Price", "required": "false", "type": "number",
                "data": "", "condition": ""},
            {"field": "opp_commission_percent", "label": "Commission Percentage",
                "required": "false", "type": "number", "data": "", "condition": ""},
            {"field": "opp_address", "label": "Address",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "true", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_settlement_date", "label": "Settlement Date", "required": "true",
             "type": "date", "data": "", "condition": ""},
        ],
        # Probably not needed
        "Appointment_Met": [
            {"field": "opp_type", "label": "Transaction Type", "required": "true",
                "type": "select", "data": "Buyer,Seller", "condition": "onChange('.opp_type > select',\'change\',\
             '{\"Buyer\":{\"display\":false,\"classes\":[\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]},\
             \"Seller\":{\"display\":true,\"classes\":[\"opp_city\",\"opp_state\",\"opp_postal_code\"]})"},
            {"field": "opp_price", "label": "Price", "required": "false", "type": "number",
                "data": "", "condition": ""},
            {"field": "opp_commission_percent", "label": "Commission Percentage",
                "required": "false", "type": "number", "data": "", "condition": ""},
            {"field": "opp_address", "label": "Address",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "true", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_settlement_date", "label": "Settlement Date",
                "required": "false", "type": "date", "data": "", "condition": ""}]
    }

    return JsonResponse(Fields)


def update_form_fields(request):
    """"
        Summary:
            Function update_form_fields used for sending fields to frontend,
            Arrange as per Transaction type.

        Parameters :
            isa_list (list): Gets isa_list from frontend using ajax call.
            existing_val : Gets the Existing value from frontend using ajax.
            osa_list: Gets osa_list form frontend using ajax.

            Transaction Type Fields JSON:
            Transaction Name:{
                {"field": "used as class name in HTML", "label": "Used as Name/Label",
                "required": "true/false #Make Field required",
                "type": "select/time/text/number/state",
                "data": "value of data in list",
                "condition": "Javascript can be passed here"},
            }

        Returns: Json of Fields
    """
    isa_list = request.GET.get("isa_list", [])
    opp_key = request.GET.get("opp_key")
    team_id = request.GET.get("team_id")
    isa_list = isa_list and json.loads(isa_list)
    isa_list = ",".join(isa_list)
    osa_list = request.GET.get("osa_list", [])
    osa_list = osa_list and json.loads(osa_list)
    osa_list = ",".join(osa_list)
    existing_val = helper.get_oppurtunity_details(opp_key, team_id)
    today = date.today().strftime('%Y%m%d')
    try:
        opp_appt_date = datetime.datetime.strptime(existing_val.get("opp_appt_date", today), '%Y%m%d').strftime('%Y-%m-%d')
    except Exception as e:
        print("Error parsing date", e)
        from dateutil import parser
        obj = parser.parse(existing_val.get("opp_appt_date", today))
        opp_appt_date = obj.strftime("%Y-%m-%d")
    print("osa_list:", osa_list)
    Fields = {
        "Appointment_Set": [
            {"field": "opp_type", "label": "Lead Type", "required": "true", "type": "select",
                "data": "Buyer,Seller", "condition": "onChange('.opp_type > select',\'change\',\
             '{\"Buyer\":{\"display\":false,\"classes\":[\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]},\
             \"Seller\":{\"display\":true,\"classes\":[\"opp_address\", \"opp_city\",\"opp_state\",\"opp_postal_code\"]}}',\
              [\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"])", "readonly": "true"},
            {"field": "opp_isa", "label": "ISA", "required": "false",
             "type": "select", "data": isa_list, "condition": ""},
            {"field": "opp_assigned_osa", "label": "OSA", "required": "false",
             "type": "select", "data": osa_list, "condition": ""},
            {"field": "opp_appt_date", "label": "Appointment Date", "required": "true",
             "type": "date", "data": "", "condition": ""},
            {"field": "appt_time", "label": "Appointment Time", "required": "true",
             "type": "time", "data": "", "condition": ""},
            {"field": "opp_address", "label": "Address",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
                "required": "true", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "true", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "true", "type": "text", "data": "", "condition": ""}],
        "Appointment_Met": [
            {"field": "opp_appt_met_date", "label": "Appointment Date", "required": "true", "value": opp_appt_date,
             "type": "date", "data": "", "condition": "", "readonly": "false"}],
        "Pending": [
            {"field": "opp_type", "label": "Lead Type", "required": "true", "type": "select",
                "data": "Buyer,Seller", "readonly": "true"},
            {"field": "opp_price", "label": "Price", "required": "false", "type": "number",
             "data": "", "condition": ""},
            {"field": "opp_commission_percent", "label": "Commission Percentage",
             "required": "false", "type": "number", "data": "", "condition": ""},
            {"field": "opp_address", "label": "Address",
             "required": "false", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
             "required": "false", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "false", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "false", "type": "text", "data": "", "condition": ""},
            {"field": "opp_under_contract_date", "label": "Under Contract Date",
             "required": "true", "type": "date", "data": "", "condition": ""},
            {"field": "opp_forecasted_close_date", "label": "Forecasted Close Date",
                "required": "false", "type": "date", "data": "", "condition": ""}],
        "Closed": [
            {"field": "opp_type", "label": "Lead Type", "required": "true", "type": "select",
                "data": "Buyer,Seller", "readonly": "true"},
            {"field": "opp_price", "label": "Price", "required": "false", "type": "number",
                "data": "", "condition": ""},
            {"field": "opp_commission_percent", "label": "Commission Percentage",
                "required": "false", "type": "number", "data": "", "condition": ""},
            {"field": "opp_address", "label": "Address",
                "required": "false", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
                "required": "false", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "false", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "false", "type": "text", "data": "", "condition": ""},
            {"field": "opp_settlement_date", "label": "Settlement Date", "required": "true",
             "type": "date", "data": "", "condition": ""},
        ],
        "Agreement_Signed": [
            {"field": "opp_type", "label": "Lead Type", "required": "true", "type": "select",
                "data": "Buyer,Seller", "readonly": "true", "condition": "onChange('.opp_type > select',\'change\',\
             '{\"Buyer\":{\"display\":false,\"classes\":[\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"]},\
             \"Seller\":{\"display\":true,\"classes\":[\"opp_address\", \"opp_city\",\"opp_state\",\"opp_postal_code\"]}}',\
              [\"opp_address\",\"opp_city\",\"opp_state\",\"opp_postal_code\"])", "readonly": "true"},
            {"field": "opp_price", "label": "Price", "required": "false", "type": "number",
                "data": "", "condition": ""},
            {"field": "opp_commission_percent", "label": "Commission Percentage",
                "required": "false", "type": "number", "data": "", "condition": ""},
            {"field": "opp_agreement_signed_date", "label": "Agreement Signed Date",
                "required": "true", "type": "date", "data": "", "condition": ""},
            {"field": "opp_agreement_expiration_date", "label": "Agreement Expiration Date",
                "required": "true", "type": "date", "data": "", "condition": ""},
            {"field": "opp_forecasted_close_date", "label": "Forecasted Close Date",
                "required": "false", "type": "date", "data": "", "condition": ""},
            {"field": "opp_address", "label": "Address",
                "required": "false", "type": "text", "data": "", "condition": ""},
            {"field": "opp_city", "label": "City",
                "required": "false", "type": "text", "data": "", "condition": ""},
            {"field": "opp_state", "label": "State",
                "required": "false", "type": "state", "data": "", "condition": ""},
            {"field": "opp_postal_code", "label": "Zip Code",
                "required": "false", "type": "text", "data": "", "condition": ""}
        ]}
    for field_key, field_value in Fields.items():
        for f in field_value:
            if f["field"] in existing_val:
                value = existing_val[f["field"]]
                f["value"] = value
                if value and f["type"] == "date" and "-" not in value:
                    f["value"] = f"{value[:4]}-{value[4:6]}-{value[-2:]}"
    return JsonResponse(Fields)


# Create your views here.
@csrf_exempt
def list_view(request):
    try:
        context = {}
        input_data = dict(request.GET)
        context_data = input_data.get("context", [])
        signature = input_data.get("signature")

        if len(context_data) > 0:
            try:
                if context_data[0][:-2] != "==":
                    context_data_decoded = base64.b64decode(context_data[0] + "==")
                else:
                    context_data_decoded = base64.b64decode(context_data[0])
                context_data_decoded = json.loads(context_data_decoded)
            except Exception:
                return HttpResponse("Something Went Wrong!!")
        domain = context_data_decoded["account"]["domain"]
        person = context_data_decoded["person"]["id"]
        status, oppurtunity_list, team_id, error = helper.get_oppurtunity_list(domain, person)
        if error:
            return render(request, 'common_form/inactive_user_error.html')
        if status is False or team_id is None:
            return render(request, 'common_form/error.html')
        # context["buyer_stage_colors"] = buyer_stage_colors
        # context["seller_stage_colors"] = seller_stage_colors
        context["team_id"] = team_id

        person_resp = helper.get_fub_user(domain)
        is_tagged = False

        # print("person resp: ----", person_resp, "-----")
        if person_resp.get("statusCode", 200) == 404 and person_resp.get(
            "message", False
        ) in ["InvalidUser", "NoDomain"]:
            # print("New User")
            return render(request, "common_form/new_user.html", {"new_user": "True"})

        hash_key = person_resp.get("secret_key", None)
        if "settings" in person_resp:
            form_type = person_resp["settings"].get("embedded_form_type", "normal")
            is_tagged = person_resp["settings"].get("is_tag_system_active", False)
            is_one_click_date = person_resp["settings"].get("is_one_click_date", False)
            chatgpt_integration = person_resp["settings"].get("chatgpt_integration", False)
            context["form_type"] = form_type
        else:
            return render(request, "common_form/error.html")

        # Opportunity Processing
        oppurtunity_list.sort(key=lambda x: x.get('opp_created_ts', '2000-01-01'), reverse=True)
        if is_tagged:
            oppurtunity_list.sort(key=lambda x: x.get('is_tagged', False), reverse=True)
        oppurtunity_list.sort(key=lambda x: x['opp_stage'] == 'Closed')
        oppurtunity_list.sort(key=lambda x: x['opp_stage'] == 'Terminated')

        context['number_of_seller_opp'] = 0
        context['number_of_buyer_opp'] = 0
        existing_opp_link_seller = {}
        existing_opp_link_buyer = {}

        for opp in oppurtunity_list:
            opp['opp_key'] = opp[OPP_KEY]
            opp_forecasted_close_date = opp.get('opp_forecasted_close_date', '')
            if opp_forecasted_close_date and "-" not in opp_forecasted_close_date:
                opp.update({'opp_forecasted_close_date':
                            f"{opp_forecasted_close_date[:4]}-{opp_forecasted_close_date[4:6]}-{opp_forecasted_close_date[-2:]}"})
            if (opp['opp_stage'] == 'Appointment Set' or opp['opp_stage'] == 'Pipeline') and \
                    opp.get('appt_set_lead_type', "") == 'BuyerSeller' and opp['opp_type'] == 'Buyer':
                opp['notshow'] = True
            else:
                opp['show'] = False
            if opp['opp_type'] == 'Seller':
                context['number_of_seller_opp'] = context['number_of_seller_opp'] + 1
            elif opp['opp_type'] == 'Buyer':
                context['number_of_buyer_opp'] = context['number_of_buyer_opp'] + 1

        for opp in oppurtunity_list:
            if (context['number_of_seller_opp'] == 1 and opp['opp_type'] == 'Seller'):
                existing_opp_link_seller = json.dumps({'stage': opp['opp_stage'], 'opp_key': opp['opp_key'], 'deal_id': opp.get('fub_deal_id'),
                                                       'team_id': team_id, 'update_form': '1'})
            if (context['number_of_buyer_opp'] == 1 and opp['opp_type'] == 'Buyer'):
                existing_opp_link_buyer = json.dumps({'stage': opp['opp_stage'], 'opp_key': opp['opp_key'], 'deal_id': opp.get('fub_deal_id'),
                                                      'team_id': team_id, 'update_form': '1'})

        context['is_tagsSystem'] = is_tagged
        context['is_one_click_date'] = is_one_click_date
        context["oppurtunity_list"] = oppurtunity_list
        context["context_data"] = context_data[0]
        context["signature"] = signature[0]
        context["STAGE"] = STAGE
        context['existing_opp_link_seller'] = existing_opp_link_seller
        context['existing_opp_link_buyer'] = existing_opp_link_buyer
        context['chatgpt_integration'] = chatgpt_integration

        status = helper.check_hash(context_data, signature, hash_key)
        if not status:
            return HttpResponse("Invalid Signature, Something went wrong!")

        if context['form_type'] == 'chatbot':
            return HttpResponseRedirect(f"../chat/list_conversations?context={context_data[0]}&signature={signature[0]}")

        return render(request, "common_form/list_view.html", context=context)
    except Exception as e:
        print(traceback.format_exc(), e)
        return render(request, 'common_form/error.html')


# Create your views here.
@csrf_exempt
def update_form(request):
    context = {}
    input_data = dict(request.GET)
    context_data = input_data.get("context", [])
    signature = input_data.get("signature")
    if len(context_data) > 0:
        try:
            if context_data[0][:-2] != "==":
                context_data_decoded = base64.b64decode(context_data[0] + "==")
            else:
                context_data_decoded = base64.b64decode(context_data[0])
            context_data_decoded = json.loads(context_data_decoded)
        except Exception:
            return HttpResponse("Something Went Wrong!!")
    domain = context_data_decoded["account"]["domain"]
    person_id = context_data_decoded["person"]["id"]
    context["fub_person_id"] = person_id
    context["context_data"] = context_data[0]
    context["signature"] = signature[0]
    team_id = request.GET.get("team_id")
    if request.method == "GET":
        opp_key = request.GET.get("opp_key")
        if opp_key:
            resp = helper.get_oppurtunity_details(opp_key, team_id)
            context.update(resp)
        context["opp_key"] = opp_key
        # Get fub users
        resp = helper.get_fub_user(domain)
        context["user_data"] = resp["data"]
        context["is_update"] = 0
        context["osa_list"] = json.dumps([i.get("name") for i in resp["data"] if i["is_osa"] is True])
        context["isa_list"] = json.dumps([
            i.get("name")
            for i in resp["data"]
            if i.get("isa_or_admin", "") == "ISA" or i.get("is_isa", False) is True
        ])
        print("context", context)
        print("context_data", context_data)

    if request.method == "POST":
        pl = request.POST.dict()
        del pl["csrfmiddlewaretoken"]
        pl["opp_type"] = pl.get("previous_opp_type")
        pl["domain"] = domain
        # Added alternate value on update "update existing opportunity"
        pl["opp_updated_ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pl["sisu_client_updated_ts"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        pl["fub_deal_entered_stage_ts"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        pl["fub_deal_stage_name"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        pl["opp_request_type"] = "updating existing transaction"
        pl["fub_person_id"] = person_id
        pl["emb_appt_version"] = 2
        pl["created_on"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        print("Main Payload \n", pl, "\n")
        resp = helper.update_oppurtunity(pl)
        return HttpResponseRedirect(
            f"../common_form/success?success=1&context={context_data[0]}&signature={signature[0]}"
        )

    person_resp = helper.get_fub_user(domain)
    hash_key = person_resp.get("secret_key", None)
    status = helper.check_hash(context_data, signature, hash_key)
    if not status:
        return HttpResponse("Invalid Signature, Something went wrong!")
    if "settings" in person_resp:
        planFubWufoo = person_resp["settings"].get("planFubWufoo", False)
        context["planFubWufoo"] = planFubWufoo
    else:
        return render(request, "common_form/error.html")
    return render(request, "common_form/update_form.html", context=context)


# Create your views here.
@csrf_exempt
def wufoo_form(request):
    context = {}
    input_data = dict(request.GET)
    context_data = input_data.get("context", [])
    signature = input_data.get("signature")
    if len(context_data) > 0:
        try:
            if context_data[0][:-2] != "==":
                context_data_decoded = base64.b64decode(context_data[0] + "==")
            else:
                context_data_decoded = base64.b64decode(context_data[0])
            context_data_decoded = json.loads(context_data_decoded)
        except Exception:
            return HttpResponse("Something Went Wrong!!")
    domain = context_data_decoded["account"]["domain"]
    person_id = context_data_decoded["person"]["id"]
    context["fub_person_id"] = person_id
    context["signature"] = signature[0]
    context["context_data"] = context_data[0]
    person_resp = helper.get_fub_user(domain)

    hash_key = person_resp.get("secret_key", None)
    team_id = person_resp.get("team_id")

    # get form links
    form_reps = helper.get_form_links(team_id=team_id, opp_key="", person_id=person_id)

    status = helper.check_hash(context_data, signature, hash_key)
    if not status:
        return HttpResponse("Invalid Signature, Something went wrong!")

    if form_reps.get("error", False):
        return HttpResponse('Please visit <a href="https://datalabz.re/" target="_blank">datalabz.re</a> to subscribe and enable the embedded App!')

    # context form links:
    # print("form_reps", form_reps)
    context.update(
        {
            "closed_url": form_reps["customClosedTransactionForm"],
            "pending_url": form_reps["customPendingTransactionForm"],
            "agreement_signed_url": form_reps["customAgreement_SignedTransactionForm"],
            "appt_set_url": form_reps["customAppointmentForm"],
            "pipeline_url": form_reps.get("customPipelineForm"),
            "terminate_url": form_reps.get("customTerminateForm"),
        }
    )
    return render(request, "common_form/wufoo_form.html", context=context)


@csrf_exempt
def update_wufoo_form(request):
    context = {}
    input_data = dict(request.GET)
    context_data = input_data.get("context", [""])
    signature = input_data.get("signature", [""])
    current_stage = input_data.get("stage", [""])[0]
    deal_id = input_data.get("deal_id", [""])[0]
    context["signature"] = signature[0]
    context["context_data"] = context_data[0]
    if len(context_data) > 0:
        try:
            if context_data[0][:-2] != "==":
                context_data_decoded = base64.b64decode(context_data[0] + "==")
            else:
                context_data_decoded = base64.b64decode(context_data[0])
            context_data_decoded = json.loads(context_data_decoded)
        except Exception:
            return HttpResponse("Something Went Wrong. Please Try Again Later!")
    domain = context_data_decoded["account"]["domain"]
    person_id = context_data_decoded["person"]["id"]
    context["fub_person_id"] = person_id
    person_resp = helper.get_fub_user(domain)
    hash_key = person_resp.get("secret_key", None)
    team_id = person_resp.get("team_id")
    status = helper.check_hash(context_data, signature, hash_key)
    opp_key = request.GET.get("opp_key")
    # get form links
    form_reps = helper.get_form_links(
        team_id=team_id, person_id=person_id, fub_deal_id=deal_id, opp_key=opp_key, is_create=False
    )
    # print(form_reps)
    if request.method == "GET":
        opp_key = request.GET.get("opp_key")
        if opp_key:
            resp = helper.get_oppurtunity_details(opp_key, team_id)
            # print("\n\n Response: ", resp)
            appointments = resp.get('appointments')
            context['appointments_count'] = appointments
            context.update(resp)
        context['opp_key'] = opp_key
        # Get fub users
        context["user_data"] = person_resp["data"]
        context["is_update"] = 0
        context["osa_list"] = [i for i in person_resp["data"] if i["is_osa"] is True]
        context["isa_list"] = [
            i
            for i in person_resp["data"]
            if i.get("isa_or_admin", "") == "ISA" or i.get("is_isa", False) is True
        ]
    if not status:
        return HttpResponse("Invalid Signature, Something went wrong!")
    if form_reps.get("error", False):
        return HttpResponse('Please visit <a href="https://datalabz.re/" target="_blank">datalabz.re</a> to subscribe and enable the embedded App!')
    # context form links:
    context.update(
        {
            "closed_url": form_reps["customClosedTransactionForm"],
            "pending_url": form_reps["customPendingTransactionForm"],
            "agreement_signed_url": form_reps["customAgreement_SignedTransactionForm"],
            "appt_met_url": form_reps.get("customDispositionForm"),
            "terminate_url": form_reps.get("customTerminateForm"),
            "appt_set_url": form_reps.get("customAppointmentForm"),
            "MoreAppointments": form_reps.get("MoreAppointments"),
        }
    )
    context["current_stage"] = current_stage
    return render(request, "common_form/wufoo_update.html", context=context)


@csrf_exempt
def appoinments(request):
    context = {}
    input_data = dict(request.GET)
    context_data = input_data.get("context", [""])
    signature = input_data.get("signature", [""])
    current_stage = input_data.get("stage", [""])[0]
    deal_id = input_data.get("deal_id", [""])[0]
    context["signature"] = signature[0]
    context["context_data"] = context_data[0]
    if len(context_data) > 0:
        try:
            if context_data[0][:-2] != "==":
                context_data_decoded = base64.b64decode(context_data[0] + "==")
            else:
                context_data_decoded = base64.b64decode(context_data[0])
            context_data_decoded = json.loads(context_data_decoded)
        except Exception:
            return HttpResponse("Something Went Wrong. Please Try Again Later!")
    domain = context_data_decoded["account"]["domain"]
    person_id = context_data_decoded["person"]["id"]
    context["fub_person_id"] = person_id
    person_resp = helper.get_fub_user(domain)
    hash_key = person_resp.get("secret_key", None)
    team_id = person_resp.get("team_id")
    status = helper.check_hash(context_data, signature, hash_key)
    opp_key = request.GET.get("opp_key")
    # get form links
    form_reps = helper.get_form_links(
        team_id=team_id, person_id=person_id, fub_deal_id=deal_id, opp_key=opp_key, is_create=False, ApptLinks=True
    )
    print("form_reps", form_reps)
    # if request.method == "GET":
    #     opp_key = request.GET.get("opp_key")
    #     if opp_key:
    #         resp = helper.get_oppurtunity_details(opp_key, team_id)
    #         # print("\n\n Response: ", resp)
    #         context.update(resp)
    #     context['opp_key'] = opp_key
    #     # Get fub users
    #     context["user_data"] = person_resp["data"]
    #     context["is_update"] = 0
    #     context["osa_list"] = [i for i in person_resp["data"] if i["is_osa"] is True]
    #     context["isa_list"] = [
    #         i
    #         for i in person_resp["data"]
    #         if i.get("isa_or_admin", "") == "ISA" or i.get("is_isa", False) is True
    #     ]
    if not status:
        return HttpResponse("Invalid Signature, Something went wrong!")

    if form_reps.get("error", False):
        return HttpResponse('Please visit <a href="https://datalabz.re/" target="_blank">datalabz.re</a> to subscribe and enable the embedded App!')

    # context form links:
    context.update(
        {
            # "appt_met_url": form_reps.get("customDispositionForm"),
            "appt_set_url": form_reps.get("customAppointmentForm"),
            "terminate_url": form_reps.get("customTerminateForm"),
        }
    )
    context["current_stage"] = current_stage
    # oppurtunity_list, buyer_stage_colors, seller_stage_colors, team_id = helper.get_oppurtunity_list(domain, person_id)

    appointments = form_reps.get("customDispositionForm")
    appointments = sorted(appointments, key=lambda i: i.get("opp_stage") == "Appointment Met")
    appt_set_count = disp_form_count = 0
    for appt in appointments:
        if appt.get('fub_appt_start_time') and isinstance(appt.get('fub_appt_start_time'), str) and (
                appt.get('opp_appt_disposition') != "Appt Met" and appt.get('opp_appt_disposition') != "Appt Missed"):
            appt_set_count += 1
            appt_datetime = appt['fub_appt_start_time'].split("T")
            appt_date = appt_datetime[0]
            appt_time = appt_datetime[1]
            appt['appt_date'] = appt_date
            appt['appt_time'] = appt_time.split("Z")[0]
            appt_location = appt.get("appt_location", "")
            appt["location"] = appt_location
            appt_type = appt.get('appt_type', "")
            appt["appt_type"] = appt_type
            today = date.today()
            current_date = today.strftime("%Y-%m-%d")
            appt['appt_set_count'] = appt_set_count
            if current_date <= appt['appt_date']:
                appt['date_status'] = True
            else:
                appt['date_status'] = False
        if appt.get('opp_stage', "") == 'Appointment Met' or appt.get('opp_stage', "") == 'Appt Missed':
            disp_form_count += 1
            met_date = appt.get("opp_appt_met_date", "")
            if met_date:
                appt["opp_appt_met_date"] = f"{met_date[:4]}-{met_date[4:6]}-{met_date[-2:]}"
            else:
                appt["opp_appt_met_date"] = met_date
            appt['disp_form_count'] = disp_form_count
    context["appointments"] = appointments
    context["appt_set_count"] = appt_set_count
    context["disp_form_count"] = disp_form_count
    # print(current_stage)
    return render(request, "common_form/multiple_appointments.html", context=context)
    # return render(request, "common_form/wufoo_update_1.html", context=context)


@csrf_exempt
def one_click_emb_app(request):
    context = {}
    input_data = dict(request.GET)
    opp_request_type = input_data.get("opp_request_type", [""])[0]
    context_data = input_data.get("context", [])
    signature = input_data.get("signature")
    if len(context_data) > 0:
        try:
            if context_data[0][:-2] != "==":
                context_data_decoded = base64.b64decode(context_data[0] + "==")
            else:
                context_data_decoded = base64.b64decode(context_data[0])
            context_data_decoded = json.loads(context_data_decoded)
        except Exception:
            return HttpResponse("Something Went Wrong!!")
    domain = context_data_decoded["account"]["domain"]
    person_id = context_data_decoded["person"]["id"]
    context["fub_person_id"] = person_id
    context["signature"] = signature[0]
    context["context_data"] = context_data[0]
    person_resp = helper.get_fub_user(domain)

    hash_key = person_resp.get("secret_key", None)
    team_id = person_resp.get("team_id")

    status = helper.check_hash(context_data, signature, hash_key)
    if not status:
        return HttpResponse("Invalid Signature, Something went wrong!")
    # context form links:
    # print("form_reps", form_reps)
    if request.method == "POST":  # True
        pl = request.POST.dict()
        pl['team_id'] = team_id
        pl['domain'] = domain
        if opp_request_type:
            pl["opp_request_type"] = "create_new_opportunity"
        else:
            pl["opp_request_type"] = "update_new_opportunity"
        pl["fub_person_id"] = person_id
        print("POST PAYLOAD", pl)
        print("Payload", pl)
        resp = helper.one_click_embedded_app(pl)
        print("resp", resp)
        return HttpResponseRedirect(
            f"../common_form/success?success=1&context={context_data[0]}&signature={signature[0]}&is_closed=1"
        )
    # print("context", context)
    return render(request, "common_form/one_click_emb_app.html", context=context)
