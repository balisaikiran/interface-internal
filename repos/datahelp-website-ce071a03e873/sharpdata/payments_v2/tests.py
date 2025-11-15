from django.test import TestCase
from uuid import uuid4


class BillingTestCase(TestCase):
    def setUp(self):
        pass

    def setupSession(self):
        session = self.client.session
        random_id = str(uuid4())
        session["team_id"] = "test_" + random_id
        session["first_name"] = "Test"
        session["last_name"] = "Case"
        session["organization_name"] = "Test_" + random_id
        session["line1"] = "Name = " + random_id
        session["state_code"] = "NY"
        session["city"] = "NY"
        session["zip"] = "10044"
        session["country"] = "US"
        session["email"] = "saurav+" + random_id + "@interface.re"
        session.save()
        return session

    def test_fub_webform_plus_month_no_addon(self):
        print(
            "\n__________ START TEST test_fub_webform_plus_month_no_addon ____________\n"
        )
        self.setupSession()
        pl = {"plan": ["FUB_WEBFORM_PLUS"], "addons": [], "duration": ["Monthly"]}
        response = self.client.post("/payments/generate_hp", pl)
        print("response: ", response.json())
        assert response.status_code == 200
        print(
            "\n__________END TEST test_fub_webform_plus_month_no_addon ____________\n"
        )

    def test_fub_webform_max_month_no_addon(self):
        print(
            "\n__________ START TEST test_fub_webform_max_month_no_addon ____________\n"
        )
        self.setupSession()
        pl = {"plan": ["FUB_WEBFORM_MAX"], "addons": [], "duration": ["Monthly"]}
        response = self.client.post("/payments/generate_hp", pl)
        print("response: ", response.json())
        assert response.status_code == 200
        print("\n__________END TEST test_fub_webform_max_month_no_addon ____________\n")

    def test_fub_webform_max_year_no_addon(self):
        print(
            "\n__________ START TEST test_fub_webform_max_year_no_addon ____________\n"
        )
        self.setupSession()
        pl = {"plan": ["FUB_WEBFORM_MAX"], "addons": [], "duration": ["Yearly"]}
        response = self.client.post("/payments/generate_hp", pl)
        print("response: ", response.json())
        assert response.status_code == 200
        print("\n__________END TEST test_fub_webform_max_year_no_addon ____________\n")

    def test_fub_webform_plus_year_no_addon(self):
        print(
            "\n__________ START TEST test_fub_webform_max_year_no_addon ____________\n"
        )
        self.setupSession()
        pl = {"plan": ["FUB_WEBFORM_PLUS"], "addons": [], "duration": ["Yearly"]}
        response = self.client.post("/payments/generate_hp", pl)
        print("response: ", response.json())
        assert response.status_code == 200
        print("\n__________END TEST test_fub_webform_max_year_no_addon ____________\n")

    def test_otc_webform_plus_month_no_addon(self):
        print(
            "\n__________ START TEST test_otc_webform_plus_month_no_addon ____________\n"
        )
        self.setupSession()
        pl = {"plan": ["OTC_WEBFORM_PLUS"], "addons": [], "duration": ["Monthly"]}
        response = self.client.post("/payments/generate_hp", pl)
        print("response: ", response.json())
        assert response.status_code == 200
        print(
            "\n__________END TEST test_otc_webform_plus_month_no_addon ____________\n"
        )

    def test_otc_webform_max_month_no_addon(self):
        print(
            "\n__________ START TEST test_otc_webform_max_month_no_addon ____________\n"
        )
        self.setupSession()
        pl = {"plan": ["OTC_WEBFORM_MAX"], "addons": [], "duration": ["Monthly"]}
        response = self.client.post("/payments/generate_hp", pl)
        print("response: ", response.json())
        assert response.status_code == 200
        print("\n__________END TEST test_otc_webform_max_month_no_addon ____________\n")

    def test_otc_webform_max_year_no_addon(self):
        print(
            "\n__________ START TEST test_otc_webform_max_year_no_addon ____________\n"
        )
        self.setupSession()
        pl = {"plan": ["OTC_WEBFORM_MAX"], "addons": [], "duration": ["Yearly"]}
        response = self.client.post("/payments/generate_hp", pl)
        print("response: ", response.json())
        assert response.status_code == 200
        print("\n__________END TEST test_otc_webform_max_year_no_addon ____________\n")

    def test_otc_webform_plus_year_no_addon(self):
        print(
            "\n__________ START TEST test_otc_webform_plus_year_no_addon ____________\n"
        )
        self.setupSession()
        pl = {"plan": ["OTC_WEBFORM_PLUS"], "addons": [], "duration": ["Yearly"]}
        response = self.client.post("/payments/generate_hp", pl)
        print("response: ", response.json())
        assert response.status_code == 200
        print("\n__________END TEST test_otc_webform_plus_year_no_addon ____________\n")
