from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from sharpdata.helper import make_lambda_call
from . import apis
import json
from django.views.decorators.clickjacking import xframe_options_exempt
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import ast
from sharpdata.helper import login_check_decorator
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token


def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response


def get_deafult_context(request):
    context = {}
    if "intercom_hmac_hash" in dict(request.session):
        context["intercom_hmac_hash"] = request.session["intercom_hmac_hash"]
    if "user_email" in dict(request.session):
        context["user_email"] = request.session["user_email"]
    return context


@login_check_decorator
def get_csrf_token(request):
    print("csrf", get_token(request))
    return JsonResponse({'csrftoken': get_token(request)})


@login_check_decorator
@require_http_methods(["GET", "POST"])
def dashboard(request):
    context = get_deafult_context(request)
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    context["AutomationBuilder"] = request.session.get("AutomationBuilder", False)
    context["FormBuilder"] = request.session.get("FormBuilder", False)
    context["planFubOtc"] = request.session.get("planFubOtc", False)
    context["planFubWufoo"] = request.session.get("planFubWufoo", False)
    context["chatgpt_integration"] = request.session.get("chatgpt_integration", False)
    context["organization_name"] = request.session.get("organization_name", "")
    return render(request, 'dashboard/index.html', context=context)


@login_check_decorator
def edit_template(request):
    context = get_deafult_context(request)
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    context["AutomationBuilder"] = request.session.get("AutomationBuilder", False)
    context["FormBuilder"] = request.session.get("FormBuilder", False)
    return render(request, 'dashboard/editTemp.html', context=context)


@login_check_decorator
@require_http_methods(["GET", "POST"])
def profile(request):
    context = dict(request.session)
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    context["AutomationBuilder"] = request.session.get("AutomationBuilder", False)
    context["FormBuilder"] = request.session.get("FormBuilder", False)
    context["planFubOtc"] = request.session.get("planFubOtc", False)
    context["planFubWufoo"] = request.session.get("planFubWufoo", False)
    context["chatgpt_integration"] = request.session.get("chatgpt_integration", False)
    # user_email = request.session.get("user_email")

    print("COntext from profile : ", context)
    return render(request, 'dashboard/profile.html', context=context)


@login_check_decorator
@require_http_methods(["GET", "POST"])
def update_profile(request):
    context = get_deafult_context(request)
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    context["AutomationBuilder"] = request.session.get("AutomationBuilder", False)
    context["FormBuilder"] = request.session.get("FormBuilder", False)
    context["planFubOtc"] = request.session.get("planFubOtc", False)
    context["planFubWufoo"] = request.session.get("planFubWufoo", False)
    context["chatgpt_integration"] = request.session.get("chatgpt_integration", False)
    if request.method == "POST":
        pl = request.POST.dict()
        pl["team_id"] = request.session.get("team_id")
        pl["user_id"] = request.session.get("team_id")
        lambda_name = apis.api.get("updateUser")
        resp = make_lambda_call(lambda_name, pl)
        resp = resp['body'] if 'body' in resp else resp
        print("update resp", resp)
        request.session["first_name"] = pl["first_name"]
        request.session["last_name"] = pl["last_name"]
        request.session["user_name"] = pl["first_name"] + " " + pl["last_name"]
        request.session["organization_name"] = pl["organization_name"]
        request.session["phone"] = pl["phone"]
        request.session["timezone"] = pl["timezone"]

    return HttpResponseRedirect("/user/profile")


@login_check_decorator
@require_http_methods(["GET", "POST"])
def credential_form(request):
    context = get_deafult_context(request)
    print("request session : ", dict(request.session))
    team_id = request.session.get("team_id")
    context["team_id"] = team_id
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    context["AutomationBuilder"] = request.session.get("AutomationBuilder", False)
    context["FormBuilder"] = request.session.get("FormBuilder", False)
    context["planFubOtc"] = request.session.get("planFubOtc", False)
    context["planFubWufoo"] = request.session.get("planFubWufoo", False)
    context["chatgpt_integration"] = request.session.get("chatgpt_integration", False)
    context["organization_name"] = request.session.get("organization_name", "")
    if request.method == "GET":
        if "is_success" in request.GET:
            context["is_success"] = request.GET["is_success"]
        if "fub_key_authorised" in request.GET:
            context["fub_key_authorised"] = request.GET["fub_key_authorised"]
        if "fub_key_unauthorised" in request.GET:
            context["fub_key_unauthorised"] = request.GET["fub_key_unauthorised"]
        print("Calling API")
        lambda_name = apis.api.get("getCred")
        req = {"team_id": team_id}
        resp = make_lambda_call(lambda_name, req, fetch_raw=True)
        print("Resp : ", resp)
        if "results" in resp:
            data = resp["results"]
            print("Data is :", data)
            context["twillio_email"] = data.get("twillio_username", "")
            context["fub_email"] = data.get("fub_username", "")
            context["SISU_username"] = data.get("SISU_username", "")
            context["twillio_password"] = data.get("twillio_password", "")
            context["fub_password"] = data.get("fub_password", "")
            context["SISU_password"] = data.get("SISU_password", "")
            context["is_cred"] = True
            context["OTC_username"] = data.get("OTC_username", "")
            context["OTC_password"] = data.get("OTC_password", "")
            context["fub_key"] = data.get("fub_key", "")
            # context["plan"] = request.session.get("user_plan")
    elif request.method == "POST":
        pl = {}
        pl["Tw_username"] = request.POST.get("Tw_username")
        pl["Tw_password"] = request.POST.get("Tw_password")
        pl["FUB_username"] = request.POST.get("FUB_username")
        pl["FUB_password"] = request.POST.get("FUB_password")
        pl["SISU_username"] = request.POST.get("SISU_username")
        pl["SISU_password"] = request.POST.get("SISU_password")
        pl["OTC_username"] = request.POST.get("OTC_username")
        pl["OTC_password"] = request.POST.get("OTC_password")
        pl["fub_key"] = request.POST.get("fub_key")
        if pl["fub_key"] == "" or pl["fub_key"] == "True":
            pl.pop("fub_key")
        req = dict(request.POST)
        print("pl: ", pl)
        pl["team_id"] = team_id
        lambda_name = apis.api.get("createCred")
        resp = make_lambda_call(lambda_name, pl, fetch_raw=True)
        print("create cerd resp is :", resp)
        lambda_name = apis.api.get("getFubDomain")
        if pl.get("fub_key"):
            response = make_lambda_call(lambda_name, {"team_id": team_id}, fetch_raw=True)
            print("responsess", response)
            if response == "FUB DOMAIN ADDED, Secondary USER KEY":
                return HttpResponseRedirect("../../user/credential_form?is_success=1&fub_key_authorised=2")
            elif response == "FUB DOMAIN ADDED":
                return HttpResponseRedirect("../../user/credential_form?is_success=1&fub_key_authorised=1")
            else:
                return HttpResponseRedirect("../../user/credential_form?is_success=1&fub_key_unauthorised=0")
        else:
            return HttpResponseRedirect("../../user/credential_form?is_success=1")
    print(context)
    return render(request, 'dashboard/Twillio_form.html', context=context)


@login_check_decorator
@require_http_methods(["GET", "POST"])
def settings(request):
    context = get_deafult_context(request)
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    context["AutomationBuilder"] = request.session.get("AutomationBuilder", False)
    context["FormBuilder"] = request.session.get("FormBuilder", False)
    context["planFubOtc"] = request.session.get("planFubOtc", False)
    context["planFubWufoo"] = request.session.get("planFubWufoo", False)
    context["chatgpt_integration"] = request.session.get("chatgpt_integration", False)
    context["organization_name"] = request.session.get("organization_name", "")
    results_to_show = ["user_plan", "sisu_fub_integration", "minutes_talk_time_sync",
                       "number_of_unique_dials_sync", "connections_sync", "sisu_conversation_duration",
                       "sisu_connection_duration_minimum", "sisu_connection_duration_maximum",
                       "csrfmiddlewaretoken", "smartlist_heatmap_report"]

    if request.method == "GET":
        # plan = request.session.get("plan").strip()

        pl = {"team_id": request.session.get("team_id")}
        lambda_name = apis.api.get("getSett")
        resp = make_lambda_call(lambda_name, pl)
        resp = resp['body'] if 'body' in resp else resp
        print("resp", resp)
        context.update(resp.get("results", {}))
        result = resp.get("results", {})
        request.session['heatmap_form_url'] = result.get('heatmap_form_url')
        results_to_hide = {}
        for k, v in resp.get("results", {}).items():
            if k not in results_to_show:
                if v in ['True', 'False']:
                    results_to_hide[k] = ast.literal_eval(v)
                else:
                    results_to_hide[k] = v

        context["results_to_hide"] = results_to_hide

        print("context ", context)

    elif request.method == "POST":
        print("Setting post data: ", request.POST.dict())
        plan = ""
        planFubTwillio = False
        planFubSisu = False
        planFubReport = False
        planFubEmbeddedApp = False
        if request.POST.get("planFubTwillio", 'False') == "True":
            planFubTwillio = True
        if request.POST.get("planFubSisu", 'False') == "True":
            planFubSisu = True
        if request.POST.get("planFubReport", 'False') == "True":
            planFubReport = True
        if request.POST.get("planFubEmbeddedApp", 'False') == "True":
            planFubEmbeddedApp = True
        pl = request.POST.dict()
        for item in ["Twillio", "Fub", "Sisu", "plan"]:
            if item in pl:
                del pl[item]

        print("plan is ", plan)
        pl["team_id"] = request.session.get("team_id")
        for k, v in dict(request.POST).items():
            print(k, v[0])
            if v[0] in ["True", "False", 'True', 'False']:
                print('Eval : ///', ast.literal_eval(v[0]))
                pl[k] = ast.literal_eval(v[0])
        # pl["sisu_fub_integration"] = request.POST.get("sisu_fub_integration") == "True"
        # pl["minutes_talk_time_sync"] = request.POST.get("minutes_talk_time_sync") == "True"
        # pl["number_of_unique_dials_sync"] = request.POST.get("number_of_unique_dials_sync") == "True"
        # pl["inbound_calls_sync"] = request.POST.get("inbound_calls_sync") == "True"
        # pl["connections_sync"] = request.POST.get("connections_sync") == "True"
        # pl['smartlist_heatmap_report'] = request.POST.get("smartlist_heatmap_report") == "True"
        # pl["planFubSisu"] = planFubSisu
        # pl["planFubTwillio"] = planFubTwillio
        # pl['planFubReport'] = planFubReport
        del pl["csrfmiddlewaretoken"]

        print("pl is :", pl)
        # url = apis.api.get("getSett")
        # resp = make_api_call(url, {"team_id": request.session.get("team_id")})
        # # print("resp", resp)
        # context.update(resp.get("results", {}))
        # result = resp.get("results", {})
        # result.update(pl)
        lambda_name = apis.api.get("updateSett")
        resp = make_lambda_call(lambda_name, pl, fetch_raw=True)
        print(resp)
        request.session["planFubSisu"] = planFubSisu
        request.session["planFubTwillio"] = planFubTwillio
        request.session['planFubReport'] = planFubReport
        request.session["planFubEmbeddedApp"] = planFubEmbeddedApp
        context["AutomationBuilder"] = request.session.get("AutomationBuilder", False)
        context["FormBuilder"] = request.session.get("FormBuilder", False)
        request.session['smartlist_heatmap_report'] = request.POST.get("smartlist_heatmap_report") == "True"
        context.update(pl)
        results_to_hide = {}
        for k, v in context.items():
            if k not in results_to_show:
                results_to_hide[k] = v

        context["results_to_hide"] = results_to_hide
    return render(request, 'dashboard/settings.html', context)


@login_check_decorator
def heatmap(request):
    context = get_deafult_context(request)
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    context["AutomationBuilder"] = request.session.get("AutomationBuilder", False)
    context["FormBuilder"] = request.session.get("FormBuilder", False)
    context['heatmap_form_url'] = request.session.get("heatmap_form_url", "")
    return render(request, 'dashboard/heatmap.html', context=context)


@xframe_options_exempt
def wufoo_heatmap(request):

    print(request.GET)
    context = get_deafult_context(request)
    data = json.dumps(dict(request.GET))
    data = data + " " + request.session.get("team_id", "")
    context['team'] = request.session.get("team_id", "")
    context["entry_id"] = dict(request.GET)['entry_id'][0]
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    print(context)
    return render(request, 'dashboard/heatmap_graph.html', context=context)


def check_if_file_available(request):
    time.sleep(5)
    if request.method == "GET":
        team_id = dict(request.GET)['team_id']
        entry_id = dict(request.GET)['entry_id']
        print(team_id, entry_id)
        lambda_name = apis.api.get("heatmap")
        pl = {
            'team_id': team_id[0],
            'team': team_id[0],
            'entry_id': entry_id[0]
        }
        resp = make_lambda_call(lambda_name, pl, fetch_raw=True)
        # check in api if the file is available
        if resp:
            return HttpResponse(resp['body'])
        else:
            return HttpResponse("0")
    else:
        return HttpResponse("-1")


@login_check_decorator
@require_http_methods(["GET", "POST"])
def fub_user_list(request):
    context = get_deafult_context(request)
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    context["AutomationBuilder"] = request.session.get("AutomationBuilder", False)
    context["FormBuilder"] = request.session.get("FormBuilder", False)
    context["planFubOtc"] = request.session.get("planFubOtc", False)
    context["planFubWufoo"] = request.session.get("planFubWufoo", False)
    context["chatgpt_integration"] = request.session.get("chatgpt_integration", False)
    if 'user_list' not in request.session:
        request.session['user_list'] = [
            {
                "fub_uid": 1,
                "name": "Saurav Panda",
                "email": "saurav@gmail.com",
                "embedded_app_access": True,
                "is_osa": True,
                "isa_or_admin": "ISA",
                "updated_on": "2021-01-04 00:00:00",
            },
            {
                "fub_uid": 2,
                "name": "Daniel Poston",
                "email": "daniel@gmail.com",
                "embedded_app_access": True,
                "is_osa": True,
                "isa_or_admin": "ADMIN",
                "updated_on": "2021-01-04 00:00:00",
            }
        ]

    if request.method == "GET":
        # fetch all the tags
        lambda_name = apis.api["list_users"]
        pl = {"team_id": request.session.get("team_id", "")}
        resp = make_lambda_call(lambda_name, pl)
        # print("User list resp: ", resp)
        resp = resp['body'] if 'body' in resp else resp
        context["user_list"] = resp["data"]
        context["team_id"] = request.session.get("team_id", "")
    return render(request, 'dashboard/fub_user_list.html', context=context)


def update_fub_user(request):
    if request.method == "POST":
        pl = {k: v[0] for k, v in dict(request.POST).items()}
        # print("Payload", pl)
        pl["is_osa"] = True if pl.get("is_osa", "off") == "on" else False
        pl["is_isa"] = True if pl.get("is_isa", "off") == "on" else False
        del pl["csrfmiddlewaretoken"]
        lambda_name = apis.api["update_user"]
        resp = make_lambda_call(lambda_name, pl)
        print(resp)
    return HttpResponseRedirect('/user/fub_user_list')


def add_fub_user(request):
    print(request.GET)
    if request.method == "GET":
        pl = {"team_id": request.session['team_id']}
        lambda_name = apis.api["add_user"]
        resp = make_lambda_call(lambda_name, pl)
        resp = resp['body'] if 'body' in resp else resp
        print(resp)
    return HttpResponseRedirect('/user/fub_user_list')


def delete_fub_user(request):
    print(request.GET)
    if request.method == "GET":
        pl = {
            "team_id": request.session['team_id'],
            "userId": dict(request.GET)['user_id'][0]
        }
        lambda_name = apis.api["remove_user"]
        resp = make_lambda_call(lambda_name, pl)
        resp = resp['body'] if 'body' in resp else resp
        print(resp)
    return HttpResponseRedirect('/user/fub_user_list')


@csrf_exempt
def helper_get_credentials(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid Setting'})
    # Check authorization
    auth_code = request.META.get('HTTP_USER_AGENT')
    if 'Retool' not in auth_code:
        return JsonResponse({'message': 'Invalid Setting'})
    # if '2taNmx4RnyqWwF8ei7dauRg2ighNztumPbMYLsZ' not in auth_code:
    #     return JsonResponse({'message': 'Invalid Setting'})
    team_id = request.POST.get('team_id')
    lambda_name = apis.api.get("getCred")
    if not team_id:
        return JsonResponse({'message': 'Invalid Parameter'})

    # Invoke the API and fetch the data
    req = {"team_id": team_id}
    resp = make_lambda_call(lambda_name, req, fetch_raw=True)
    return JsonResponse(resp)


@csrf_exempt
def helper_update_credentials(request):
    # Check authorization
    auth_code = request.META.get('HTTP_USER_AGENT')
    if 'Retool' not in auth_code:
        return JsonResponse({'message': 'Invalid Setting'})
    team_id = request.POST.get('team_id')
    lambda_name = apis.api.get("createCred")
    if not team_id:
        return JsonResponse({'message': 'Invalid Parameter'})

    # Invoke the API and fetch the data
    req = {k: v[0] for k, v in dict(request.POST).items()}
    print('Current post data', req)
    resp = make_lambda_call(lambda_name, req, fetch_raw=True)
    return JsonResponse(resp)


@csrf_exempt
def helper_delete_credentials(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid Setting'})
    # Check authorization
    auth_code = request.META.get('HTTP_USER_AGENT')
    if 'Retool' not in auth_code:
        return JsonResponse({'message': 'Invalid Setting'})
    team_id = request.POST.get('team_id')
    lambda_name = apis.api.get("deleteCred")
    if not team_id:
        return JsonResponse({'message': 'Invalid Parameter'})

    # Invoke the API and fetch the data
    req_params = {k: v[0] for k, v in dict(request.POST).items()}
    print(req_params)
    resp = make_lambda_call(lambda_name, req_params, fetch_raw=True)
    return JsonResponse(resp)


@csrf_exempt
def helper_transfer_property_fields(request):
    # Check authorization
    auth_code = request.META.get('HTTP_USER_AGENT')
    if 'Retool' not in auth_code:
        return JsonResponse({'message': 'Invalid Setting'})
    lambda_name = apis.api.get("transferPropertyFields")

    # Invoke the API and fetch the data
    req = {k: v[0] for k, v in dict(request.POST).items()}
    print('Current post data', req)
    resp = make_lambda_call(lambda_name, req, fetch_raw=True)
    return JsonResponse(resp)


@csrf_exempt
def helper_webhook(request):
    # Check authorization
    auth_code = request.META.get('HTTP_USER_AGENT')
    if 'Retool' not in auth_code:
        return JsonResponse({'message': 'Invalid Setting'})
    lambda_name = apis.api.get("fubWebhooks")

    # Invoke the API and fetch the data
    req = {k: v[0] for k, v in dict(request.POST).items()}
    print('Current post data', req)
    resp = make_lambda_call(lambda_name, req, fetch_raw=True)
    return JsonResponse(resp)


@csrf_exempt
def helper_custom_activity_creation(request):
    auth_code = request.META.get('HTTP_USER_AGENT')
    if 'Retool' not in auth_code:
        return JsonResponse({'message': 'Invalid Setting'})
    lambda_name = apis.api.get("createCustomActivity")
    req = {k: v[0] for k, v in dict(request.POST).items()}
    print('Current post data', req)
    resp = make_lambda_call(lambda_name, req, fetch_raw=True)
    return JsonResponse(resp)


@csrf_exempt
def helper_sisu_custom_fields(request):

    auth_code = request.META.get('HTTP_USER_AGENT')
    if 'Retool' not in auth_code:
        return JsonResponse({'message': 'Invalid Setting'})
    lambda_name = apis.api.get("sisu_custom_fields")
    params = {k: v[0] for k, v in dict(request.POST).items()}
    print('Current post data', params)
    resp = make_lambda_call(lambda_name, params, fetch_raw=True)
    return JsonResponse(resp)


@csrf_exempt
def helper_twilio_fub_webhooks(request):
    auth_code = request.META.get('HTTP_USER_AGENT')
    if 'Retool' not in auth_code:
        return JsonResponse({'message': 'Invalid Setting'})
    lambda_name = apis.api.get("twilioFubWebhooks")
    params = {k: v[0] for k, v in dict(request.POST).items()}
    print('Current post data', params)
    resp = make_lambda_call(lambda_name, params, fetch_raw=True)
    return JsonResponse(resp)


@csrf_exempt
def helper_lambda_invoker(request):
    print('Request', request.POST)
    auth_code = request.META.get('HTTP_USER_AGENT')
    print('Auth code', auth_code)
    if 'Retool' not in auth_code:
        return JsonResponse({'message': 'Invalid Setting'})
    params = {k: v[0] for k, v in dict(request.POST).items()}
    print('Current post data', params)
    lambda_function = params.get('lambda_function')
    lambda_name = apis.api.get(lambda_function)
    resp = make_lambda_call(lambda_name, params, fetch_raw=True)
    return JsonResponse(resp)


@login_check_decorator
def test_action(request):
    lambda_name = apis.api.get("TestAction")
    if request.method == "POST":
        if request.body:
            params = json.loads(request.body)
        else:
            print("request post")
            params = dict(request.POST)
        print("params", params)
        team_id = request.session.get('team_id')
        action_id = params.get('action_id')
        workflow_id = params.get('workflow_id')
        trigger_id = params.get('trigger_id')
        pl = {
            'team_id': team_id,
            'action_id': action_id,
            'workflow_id': workflow_id,
            'trigger_id': trigger_id
        }
        print("payload", pl)
        resp = make_lambda_call(lambda_name, pl)
        print("action test resp", resp)
        return JsonResponse(resp, safe=False)
    else:
        return JsonResponse({'message': 'Invalid Method'})


# @login_check_decorator
def get_user(request):
    if not request.session.get("is_loggedin"):
        JsonResponse({"is_loggedin": False})
    if request.method == "GET":
        # lambda_name = apis.api.get("getUser")
        pl = {
            'team_id': request.session.get('team_id'),
            "is_loggedin": True
        }
        # resp = make_lambda_call(lambda_name, pl)
        # print("resp", resp)
        return JsonResponse(pl, safe=False)
    else:
        return JsonResponse({'message': 'Invalid Method'})


@login_check_decorator
def get_fub_domain(request):
    print(request.GET)
    if request.method == "GET":
        pl = {
            "team_id": request.session['team_id']
        }
        lambda_name = apis.api["getFubDomain"]
        resp = make_lambda_call(lambda_name, pl)
        resp = resp['body'] if 'body' in resp else resp
        print("RESP:::", resp)
        return JsonResponse(resp, safe=False)


# def chargeebee_checkout_page(request):
#     print(request.GET)
#     return render(request, 'payments/webinar_checkout_page.html', context={})
