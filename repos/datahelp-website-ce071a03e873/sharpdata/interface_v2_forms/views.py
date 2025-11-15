from django.shortcuts import render
import traceback
import base64
from interface_v2_forms import helper
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


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


@csrf_exempt
def interface_list_view(request):
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
        person_id = context_data_decoded["person"]["id"]
        status, oppurtunity_listt, team_id, error = helper.get_oppurtunity_list(domain, person_id)
        print("person_id", person_id)
        oppurtunity_list = helper.getOpps(team_id, person_id)
        print("oppurtunity_list:", type(oppurtunity_list))
        print("error:", error, team_id, domain, person_id)
        if error:
            return render(request, 'common_form/inactive_user_error.html')
        if status is False or team_id is None:
            return render(request, 'common_form/error.html')
        context["team_id"] = team_id

        person_resp = helper.get_fub_user(domain)
        is_tagged = False

        if person_resp.get("statusCode", 200) == 404 and person_resp.get(
            "message", False
        ) in ["InvalidUser", "NoDomain"]:
            return render(request, "common_form/new_user.html", {"new_user": "True"})

        hash_key = person_resp.get("secret_key", None)
        if "settings" in person_resp:
            # form_type = person_resp["settings"].get("embedded_form_type", "normal")
            is_tagged = person_resp["settings"].get("is_tag_system_active", False)
            is_one_click_date = person_resp["settings"].get("is_one_click_date", False)
            chatgpt_integration = person_resp["settings"].get("chatgpt_integration", False)
            context["form_type"] = "wufoo_link"
            context["interface_forms"] = False
        else:
            return render(request, "common_form/error.html")

        # Opportunity Processing
        # oppurtunity_list.sort(key=lambda x: x.get('opp_created_ts', '2000-01-01'), reverse=True)
        if is_tagged:
            oppurtunity_list.sort(key=lambda x: x.get('is_tagged', False), reverse=True)
        oppurtunity_list.sort(key=lambda x: x['opp_stage'] == 'Closed')
        oppurtunity_list.sort(key=lambda x: x['opp_stage'] == 'Terminated')

        context['number_of_seller_opp'] = 0
        context['number_of_buyer_opp'] = 0
        existing_opp_link_seller = {}
        existing_opp_link_buyer = {}

        for opp in oppurtunity_list:
            opp['opp_key'] = opp.get("opp_key")
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

        return render(request, "interface_v2_forms/list_view.html", context=context)
    except Exception as e:
        print(traceback.format_exc(), e)
        return render(request, 'common_form/error.html')


@csrf_exempt
def interface_form(request):
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
    context["interface_forms"] = False
    person_resp = helper.get_fub_user(domain)

    hash_key = person_resp.get("secret_key", None)
    team_id = person_resp.get("team_id")
    fub_pipelines = helper.get_fub_pipelines(team_id)
    formlist, form_base_url = helper.getForms(team_id=team_id)
    form_links = {}
    for form in formlist:
        form_name = form.get('form_name')
        form_url = f"{form_base_url}forms/{form.get('form_id')}?InputField-Follow-up-boss-lead-id={str(person_id)}"
        form_links[form_name] = form_url
    context["interface_formlinks"] = form_links
    context["fub_pipelines"] = fub_pipelines
    status = helper.check_hash(context_data, signature, hash_key)
    if not status:
        return HttpResponse("Invalid Signature, Something went wrong!")
    return render(request, "interface_v2_forms/interface_form.html", context=context)


@csrf_exempt
def update_interface_form(request):
    context = {}
    input_data = dict(request.GET)
    context_data = input_data.get("context", [""])
    signature = input_data.get("signature", [""])
    opp_key = input_data.get("opp_key", [""])[0]
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
    team_id = person_resp.get("team_id")
    fub_pipelines = helper.get_fub_pipelines(team_id)
    formlist, form_base_url = helper.getForms(team_id=team_id)
    form_links = {}
    for form in formlist:
        form_name = form.get('form_name')
        form_url = f"{form_base_url}forms/{form.get('form_id')}?InputField-opp-key={opp_key}&InputField-Follow-up-boss-lead-id={str(person_id)}"
        form_links[form_name] = form_url
    context["interface_formlinks"] = form_links
    context["fub_pipelines"] = fub_pipelines
    return render(request, "interface_v2_forms/update_interface_form.html", context=context)
