import chargebee
import json
import boto3
from payments.plans import p
from users.apis import api
from sharpdata.helper import make_lambda_call
try:
    f = open("/var/www/config", "r")
    data = json.loads(f.read())
    f.close()
    STAGE = data.get('STAGE', 'dev')
except Exception as e:
    print(e)
    STAGE = "dev"


# Create your views here.
# Read chargebee creds from SSM Params
client = boto3.client('ssm', region_name='us-west-2')
response = client.get_parameter(
    Name=f'{STAGE}_chargebee_key',
    WithDecryption=True
)
chargebee_key = response["Parameter"]["Value"]
# TODO: Uncomment this
chargebee_website = "datahelp"  # if STAGE=='prod' else "datahelp-test"
chargebee.configure(chargebee_key, chargebee_website)


def get_hosted_page_link(payload):
    result = chargebee.HostedPage.checkout_new(payload)
    return result


def add_sisu_otc_plans(collapsable, PLAN_CATEGORY):
    res = []
    if collapsable == "FUB_SISU":
        # add sisu add on
        res.append({"id": p["ADDON_FUB_SISU_INTE" + PLAN_CATEGORY]["id"]})
        res.append({"id": p["ADDON_FUB_SISU_INTE" + PLAN_CATEGORY]["setup_fee"]})
    elif collapsable == "FUB_OTC":
        # add otc add on
        res.append({"id": p["ADDON_FUB_OTC_INT" + PLAN_CATEGORY]["id"]})
        res.append({"id": p["ADDON_FUB_OTC_INT" + PLAN_CATEGORY]["setup_fee"]})
    elif collapsable == "FUB_SISU_OTC":
        # add otc add on
        res.append({"id": p["ADDON_FUB_SISU_OTC" + PLAN_CATEGORY]["id"]})
        res.append({"id": p["ADDON_FUB_SISU_OTC" + PLAN_CATEGORY]["setup_fee"]})
    return res


def parse_input_form(payload):
    print("Input Json Paylaod, ", json.dumps(payload, indent=2))
    add_on_list = []
    PLAN_CATEGORY = ""
    plan_id = payload["plan_id"][0]
    if "MAX" in payload["plan_id"][0]:
        PLAN_CATEGORY = "_MAX"
    elif "PLUS" in payload["plan_id"][0]:
        PLAN_CATEGORY = "_PLUS"

    # collapsable = payload["collapsable"][0]
    # if PLAN_CATEGORY:
    #     add_on_list.extend(add_sisu_otc_plans(collapsable, PLAN_CATEGORY))
    if "addon_sisu_bi_directional_sync" in payload:
        add_on_list.append({"id": p['ADDON_SISU_BIDIRECTIONAL' + PLAN_CATEGORY]["id"]})
        add_on_list.append({"id": p['ADDON_SISU_BIDIRECTIONAL' + PLAN_CATEGORY]["setup_fee"]})

    if plan_id != "FUB_EMBEDDED_APP":
        if PLAN_CATEGORY == "_PLUS":
            add_on_list.append({"id": p["ADDON_DISPOSITION_TEXT"]["id"]})

        if "addon_assignment" in payload:
            add_on_list.append({"id": p['ADDON_ASSIGNMENT_FORM']["id"]})
        if "addon_custom_branded_theme" in payload and PLAN_CATEGORY != "_MAX":
            add_on_list.append({"id": p['ADDON_CUSTOM_THEME']["id"]})
        if "addon_custom_thank_you_message" in payload and PLAN_CATEGORY != "_MAX":
            add_on_list.append({"id": p['ADDON_CUSTOM_THANKS']["id"]})
        if "addon_appointment_template" in payload and PLAN_CATEGORY != "_MAX":
            add_on_list.append(
                {
                    "id": p['ADDON_APP_DESC' + PLAN_CATEGORY]["id"], "quantity": payload["addon_appointment_template_select"][0]
                }
            )
        if "addon_document_upload_for_forms" in payload and PLAN_CATEGORY != "_MAX":
            add_on_list.append({"id": p['ADDON_DOCUMENT_UPLOAD']["id"]})
        if "addon_additional_custom_fields_that_sync_with_sisu" in payload:
            add_on_list.append({
                "id": p['ADDON_SISU_CUSTOM_FIELDS' + PLAN_CATEGORY]["id"],
                "quantity": payload["addon_additional_custom_fields_that_sync_with_sisu_select"][0]
            })
            add_on_list.append({"id": p['ADDON_SISU_CUSTOM_FIELDS' + PLAN_CATEGORY]["setup_fee"]})
        if "addon_additional_custom_fields_that_sync_with_otc" in payload:
            add_on_list.append({
                "id": p['ADDON_OTC_CUSTOM_FIELDS' + PLAN_CATEGORY]["id"],
                "quantity": payload["addon_additional_custom_fields_that_sync_with_otc_select"][0]
            })
            add_on_list.append({"id": p['ADDON_OTC_CUSTOM_FIELDS' + PLAN_CATEGORY]["setup_fee"]})
        if "addon_additional_option_fields" in payload:
            add_on_list.append(
                {
                    "id": p['ADDON_OPTIONAL_FILED' + PLAN_CATEGORY]["id"],
                    "quantity": payload["addon_additional_option_fields_select"][0]
                }
            )
            add_on_list.append({"id": p['ADDON_OPTIONAL_FILED' + PLAN_CATEGORY]["setup_fee"]})
        if "addon_additional_optional_automation" in payload:
            add_on_list.append(
                {
                    "id": p['ADDON_OPTIONAL_AUTOMATION' + PLAN_CATEGORY]["id"],
                    "quantity": payload["addon_additional_optional_automation_select"][0]
                }
            )
            add_on_list.append({"id": p['ADDON_OPTIONAL_AUTOMATION' + PLAN_CATEGORY]["setup_fee"]})

        if "addon_otc_bi_directional_sync" in payload:
            add_on_list.append({"id": p['ADDON_OTC_BIDIRECTIONAL' + PLAN_CATEGORY]["id"]})
            add_on_list.append({"id": p['ADDON_OTC_BIDIRECTIONAL' + PLAN_CATEGORY]["setup_fee"]})

    return add_on_list


def create_subscription_pl(plan_id, plan_cat):
    pl = {}
    if plan_id != "FUB_EMBEDDED_APP":
        plan_id = f'{plan_cat}_{plan_id}'
    pl["subscription"] = {
        "plan_id": p[plan_id],
    }
    return pl


def get_latest_settings(team_id):
    pl = {"team_id": team_id}
    lambda_name = api.get("getSett")
    response = make_lambda_call(lambda_name, pl)
    response = response['results'] if 'results' in response else response
    return response
