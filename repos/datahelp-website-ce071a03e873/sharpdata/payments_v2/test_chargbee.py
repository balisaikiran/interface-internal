# import unittest
# import json
# from payments_v2.helper import generate_random_customer
# from payments_v2.helper import chargebee


# class TestStringMethods(unittest.TestCase):

#     def test_embedded_app_plan(self):
#         print("\n__________ START TEST test_access_to_home_with_location ____________\n")
#         new_pl = generate_random_customer()
#         new_pl["subscription_items"] = [
#             {
#                 "item_price_id" :"SISU-Integration-USD-Monthly"
#             },
#             {
#                 "item_price_id" :"Bidirectional-Sync-Embedded-App-USD-Monthly"
#             }
#         ]

#         print(new_pl)
#         result = chargebee.HostedPage.checkout_new_for_items(new_pl)
#         print(result)
#         print("\n__________ END TEST test_access_to_home_with_location ____________\n")

#     def test_webform_plus_plan(self):
#         print("\n__________ START TEST test_webform_plus_plan ____________\n")
#         new_pl = generate_random_customer()
#         new_pl["subscription_items"] = [
#             {
#                 "item_price_id" :"Webform-Pipeline-Plus-USD-Monthly"
#             },
#             {
#                 "item_price_id" :"FUB-Webform-Additional-SISU-Fields-USD-Monthly",
#                 "quantity": 1
#             },
#             {
#                 "item_price_id": "Fub-Webform-Setup-Fee-19-USD",
#                 "item_type": "charge",
#                 "charge_once": True,
#                 "charge_on_option" : "immediately"
#             }
#         ]

#         print(new_pl)
#         result = chargebee.HostedPage.checkout_new_for_items(new_pl)
#         print(result)
#         print("\n__________ END TEST test_access_to_home_with_location ____________\n")
