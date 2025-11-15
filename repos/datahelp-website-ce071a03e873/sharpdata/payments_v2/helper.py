import chargebee
import json
from . import plans
import uuid

# Create your views here.
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
    chargebee_key = None
    chargebee_site = "datahelp-test"
chargebee.configure(chargebee_key, chargebee_site)


p = plans.p


def create_customer(team_id, first_name, last_name, email, phone):

    chargebee.Customer.create(
        {
            "id": team_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
        }
    )

    return True


def create_subscription(plan, duration, addons):
    charges = []
    charges.append({"item_price_id": f"{p[plan]}-{duration}"})
    # Add plan setup fee
    if duration == "Monthly":
        if f"{plan}_SETUP" in p:
            charges.append({"item_price_id": p[f"{plan}_SETUP"], "charge_once": True})

    # Attach Addons
    if "OTC" in plan:
        all_addons = p["OTC_ADDONS"]
    elif "FUB" in plan:
        all_addons = p["FUB_ADDONS"]
    else:
        all_addons = p["EMBEDDED_APP_ADDONs"]
    for k, v in addons.items():
        if "addon_" not in k:
            continue

        item = k.replace("addon_", "")
        try:
            quantity = int(v[0])
        except Exception as e:
            print(e)
            quantity = 0
        addon_info = all_addons[item]
        if quantity:
            charges.append(
                {
                    "item_price_id": addon_info["addon"] + "-" + duration,
                    "quantity": quantity,
                }
            )
        else:
            charges.append({"item_price_id": addon_info["addon"] + "-" + duration})
        if addon_info["setup_fee"]:
            charges.append({"item_price_id": addon_info[plan]})

    return charges


def remove_mandatory_items(plan, duration, addons):
    items = p[f"ALL_{plan}"]

    if duration == "Monthly":
        if f"{plan}_SETUP" in p:
            items.remove(p[f"{plan}_SETUP"])
    return items


def generate_random_customer():
    pl = {
        "redirect_url": "https://sandbox.datalabz.re/test",
    }
    random_id = str(uuid.uuid4())
    pl["customer"] = {
        "id": "test_" + random_id,
        "email": f"saurav+{random_id}@interface.re",
        "first_name": "test",
        "last_name": "test",
        "company": f"test {random_id}",
    }
    pl["billing_address"] = {
        "email": pl["customer"]["email"],
        "first_name": pl["customer"]["first_name"],
        "last_name": pl["customer"]["last_name"],
        "company": pl["customer"]["company"],
        "phone": "+19167388937",
        "line1": "Test",
        "state_code": "NY",
        "city": "NY",
        "zip": "10001",
        "country": "US",
    }
    return pl
