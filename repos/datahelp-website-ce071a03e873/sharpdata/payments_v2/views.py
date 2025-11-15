import traceback
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from . import helper
import chargebee
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from sharpdata.helper import login_check_decorator

try:
    f = open("/var/www/config", "r")
    data = json.loads(f.read())
    f.close()
    STAGE = data.get("STAGE", "dev")
    chargebee_key = data.get("chargebee_key")
    chargebee_site = data.get("chargebee_site")
except Exception as e:
    print(e)
    STAGE = "dev"
    chargebee_key = ""
    chargebee_site = "datahelp-test"

# Create your views here.
chargebee.configure(chargebee_key, chargebee_site)


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
    if "state" in pl:
        state = pl["state"][0]
    return HttpResponseRedirect(f"/payments/billing?state={state}&plan_id={plan_id}")


@login_check_decorator
def billing(request):
    # print(dict(request.META))
    context = {}
    context["website_name"] = chargebee_site
    return render(request, "dashboard/billing.html", context=context)


@csrf_exempt
def generate_hp(request):
    data = dict(request.POST)
    plan = data["plan"][0]
    duration = data["duration"][0]
    print("Input data: ", data)

    try:
        HTTP_REFERER = dict(request.META)["HTTP_REFERER"]
    except Exception as e:
        print(e)
        HTTP_REFERER = "https://datalabz.re/"
    print(HTTP_REFERER)
    base_url = HTTP_REFERER.split("//")[-1].split("/")[0]
    redirect_url = f'{HTTP_REFERER.split("//")[0]}//{base_url}/payments/billing/{plan}'
    print(redirect_url)
    chargebee_pl = {
        "redirect_url": redirect_url,
        "subscription_items": [],
        "customer": {
            "id": request.session.get("team_id"),
            "email": request.session.get("user_email"),
            "first_name": request.session.get("first_name"),
            "last_name": request.session.get("last_name"),
            "company": request.session.get("organization_name"),
        }
    }

    chargebee_pl["subscription_items"] = helper.create_subscription(
        plan, duration, data
    )
    # chargebee_pl["mandatory_items_to_remove"] = helper.remove_mandatory_items(plan, duration, addons)
    print("input payload: ", chargebee_pl)
    try:
        result = chargebee.HostedPage.checkout_new_for_items(chargebee_pl)
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
    return JsonResponse(hosted_page)
