import boto3
import json
from django.http import HttpResponseRedirect

lambda_client = boto3.client("lambda", region_name="us-west-2")


def make_lambda_call(lambda_name, payload, fetch_raw=False):
    """
    This function is used to make api calls.
    Input: lambda_name - name of lambda url to be called
            payload - payload to be posted to API
    Output: event - API response in json format
    """

    # Make a post request
    response = lambda_client.invoke(
        FunctionName=lambda_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    event = json.loads(response["Payload"].read())
    if "headers" in event or "body" in event:
        if "body" in event:
            if isinstance(event["body"], dict):
                return event["body"]
        body = event.get("body", "{}") or "{}"
        event = json.loads(body)
    return event


def login_check_decorator(called_function):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("is_loggedin"):
            return HttpResponseRedirect("/secure/login_user")
        else:
            if not request.session.get("intercom_hmac_hash"):
                import hmac
                import hashlib

                request.session["intercom_hmac_hash"] = hmac.new(
                    b"ipOwn2jNgvbABGtLwFenzRVVeNtOdqLVURHys7mI",  # secret key (keep safe!)
                    bytes(
                        request.session.get("user_email"), encoding="utf-8"
                    ),  # user's email address
                    digestmod=hashlib.sha256,  # hash function
                ).hexdigest()
            return called_function(request, *args, **kwargs)

    wrapper.__doc__ = called_function.__doc__
    wrapper.__name__ = called_function.__name__
    return wrapper
