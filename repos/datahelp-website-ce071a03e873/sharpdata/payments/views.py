import traceback
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from . import helper
import chargebee
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from sharpdata.helper import login_check_decorator
from django.views.decorators.http import require_http_methods


@csrf_exempt
def success(request):
    context = {}
    context["organization_name"] = request.session.get("organization_name", "")
    context["team_id"] = request.session.get("team_id", "")
    return render(request, "payments/success.html", context=context)


def plans(request):
    print(dict(request.META))
    context = {}
    entries = chargebee.Plan.list({"limit": 10, "status[is]": "active"})
    webform_plans = []
    other_plans = []
    for ent in entries:
        if "fub-webform" in ent.plan.id:
            webform_plans.append(
                {
                    "name": ent.plan.name,
                    "price": int(ent.plan.price / 100),
                    "description": ent.plan.description,
                    "setup_cost": int((ent.plan.setup_cost or 0) / 100),
                }
            )
        else:
            other_plans.append(
                {
                    "name": ent.plan.name,
                    "price": int(ent.plan.price / 100),
                    "description": ent.plan.description,
                    "setup_cost": int((ent.plan.setup_cost or 0) / 100),
                }
            )
    context["webform_plans"] = webform_plans
    context["other_plans"] = other_plans
    return render(request, "dashboard/plans.html", context=context)


def billing_plans(request, plan_id):
    pl = dict(request.GET)
    state = ""
    request.session["conversion"] = "true"
    if "state" in pl:
        state = pl["state"][0]
    return HttpResponseRedirect(f"/payments/billing?state={state}&plan_id={plan_id}")


@login_check_decorator
@require_http_methods(["GET", "POST"])
def billing(request):
    context = {}
    latest_settings = helper.get_latest_settings(request.session["team_id"])
    print("latest_settings", latest_settings)
    context["has_active_plan"] = latest_settings.get("has_active_plan", False)
    request.session["AutomationBuilder"] = latest_settings.get("AutomationBuilder", False)
    request.session["FormBuilder"] = latest_settings.get("FormBuilder", False)
    # context["plan_category"] = latest_settings.get("plan_category", "")
    context["plan_type"] = ""
    if "max" in latest_settings.get("current_active_plan", ""):
        context["plan_type"] = "MAX"
    elif "plus" in latest_settings.get("current_active_plan", ""):
        context["plan_type"] = "PLUS"

    A = latest_settings.get("planFubEmbeddedApp", False)
    B = latest_settings.get("planFubTwillio", False)
    C = latest_settings.get("planFubSisu", False)
    D = latest_settings.get("planFubWufoo", False)
    context["planFubEmbeddedApp"] = A
    context["planFubTwillio"] = B
    context["planFubSisu"] = C
    context["planFubWufoo"] = D
    context["planFubOtc"] = latest_settings.get("planFubOtc", False)
    context["chatgpt_integration"] = latest_settings.get("chatgpt_integration", False)
    context["organization_name"] = request.session.get("organization_name", "")
    context["first_name"] = request.session.get("first_name", "")
    context["last_name"] = request.session.get("last_name", "")
    context["user_email"] = request.session.get("user_email", "")
    context["team_id"] = request.session.get("team_id", "")
    context["AutomationBuilder"] = latest_settings.get("AutomationBuilder", False)
    context["FormBuilder"] = latest_settings.get("FormBuilder", False)

    # if latest_settings.get("current_active_plan", "") == "":
    if A or B or C or D:
        context["has_active_plan"] = True
        context["plan_category"] = "OLD FUB Plan"

    if "plan_category" in latest_settings:
        context["plan_category"] = latest_settings.get("plan_category", "")

    if request.method == "GET":
        state = request.GET.get("state", "")
        context["payment_state"] = state
        if state == "succeeded":
            return HttpResponseRedirect("../success")
        if state == "refresh":
            request.session["planFubTwillio"] = latest_settings.get("planFubTwillio", False)
            request.session["embedded_form_type"] = latest_settings.get("embedded_form_type", "normal")
            request.session["planFubSisu"] = latest_settings.get("planFubSisu", False)
            request.session["planFubReport"] = latest_settings.get("planFubReport", False)
            request.session["smartlist_heatmap_report"] = latest_settings.get("smartlist_heatmap_report", False)
            request.session["planFubEmbeddedApp"] = latest_settings.get("planFubEmbeddedApp", False)
            request.session['heatmap_form_url'] = latest_settings.get("heatmap_form_url", "")
            request.session['subscription_status'] = latest_settings.get('status')
            request.session["planFubOtc"] = latest_settings.get("planFubOtc", False)
            request.session["chatgpt_integration"] = latest_settings.get("chatgpt_integration", False)
            request.session["planFubWufoo"] = latest_settings.get("planFubWufoo", False)
            request.session["AutomationBuilder"] = latest_settings.get("AutomationBuilder", False)
            request.session["FormBuilder"] = latest_settings.get("FormBuilder", False)
        if "has_payment" in request.GET:
            context["has_payment"] = True
            context["hosted_page_url"] = request.session.get("hosted_page_url", "")
            context["chargebee_website"] = helper.chargebee_website
    context['conversion'] = request.session.get("conversion")
    print("CONVERSION", context['conversion'])
    # request.session.pop("conversion", None)

    return render(request, "payments/billing.html", context=context)


@login_check_decorator
def generate_hp(request):
    print(request.POST)
    data = dict(request.POST)
    plan_id = data["plan_id"][0]
    HTTP_REFERER = dict(request.META)["HTTP_REFERER"]
    base_url = HTTP_REFERER.split("//")[-1].split("/")[0]
    redirect_url = (
        f'{HTTP_REFERER.split("//")[0]}//{base_url}/payments/billing/?plan_id={plan_id}'
    )
    chargebee_pl = {
        "redirect_url": redirect_url,
        "customer": {
            "id": request.session.get("team_id"),
            "email": request.session.get("user_email"),
            "first_name": request.session.get("first_name"),
            "last_name": request.session.get("last_name"),
            "company": request.session.get("organization_name"),
        }
    }

    plan_cat = data["collapsable"][0]

    chargebee_pl.update(helper.create_subscription_pl(plan_id, plan_cat))
    chargebee_pl["addons"] = helper.parse_input_form(data)
    print("Chargebee Payload: ", json.dumps(chargebee_pl, indent=2))
    try:
        result = helper.get_hosted_page_link(chargebee_pl)
    except Exception as e:
        e = str(e)
        print(e)
        print("Chargebee error")
        url = "https://hooks.slack.com/services/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"

        pl = {
            "text": f"Chargebee Error {e},\n Chargebee Payload: {json.dumps(chargebee_pl)}\n Error: {traceback.format_exc()}"
        }
        # print("500 error Request meta", request.META)
        try:
            import requests

            requests.post(url, json=pl)
        except Exception:
            # print(traceback.format_exc())
            pass
        error = e.split("chargebee.api_error.InvalidRequestError")[-1]
        return JsonResponse(error)
    hosted_page = result._response["hosted_page"]
    print("output hosted page: ", hosted_page)
    request.session["hosted_page_url"] = hosted_page
    return HttpResponseRedirect("/payments/billing?has_payment=1")


@csrf_exempt
def get_hosted_page(request):
    print(request.session["hosted_page_url"])
    return JsonResponse(request.session["hosted_page_url"])


@login_check_decorator
@require_http_methods(["GET", "POST"])
def fubcon_billing(request):
    context = {}
    context["organization_name"] = request.session.get("organization_name", "")
    context["first_name"] = request.session.get("first_name", "")
    context["last_name"] = request.session.get("last_name", "")
    context["user_email"] = request.session.get("user_email", "")
    context["team_id"] = request.session.get("team_id", "")

    if request.method == "GET":
        state = request.GET.get("state", "")
        context["payment_state"] = state
        if state == "succeeded":
            return HttpResponseRedirect("../success")

        if "has_payment" in request.GET:
            context["has_payment"] = True
            context["hosted_page_url"] = request.session.get("hosted_page_url", "")
            context["chargebee_website"] = helper.chargebee_website

    return render(request, "payments/billing_fubcon.html", context=context)
