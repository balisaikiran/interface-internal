from django.shortcuts import render
from django.http import HttpResponseRedirect
# from login.aws_cognito import creating_user ,loging_user ,verifying_user
import datetime
from . import apis
from sharpdata.helper import make_lambda_call
from django.http import JsonResponse
import re
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
from django.views.decorators.http import require_http_methods


def send_slack_notification_create_user(error, pl, is_retool=False):
    import json

    url = "https://hooks.slack.com/services/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"
    paylaod = {
        "text": f"Create User Error: {error},\n User Payload: {json.dumps(pl)}, is_retool: {is_retool}"}
    try:
        import requests
        requests.post(url, json=paylaod)
    except Exception as e:
        print("Slack Notification Failed: ", e)
    raise Exception('Something went wrong!')


@require_http_methods(["GET", "POST"])
def create_user(request):
    context = {}
    message_dict = {
        "UserExists": "User with this email already exists!",
        "InvalidPhone": "Phone number is not in correct format!",
        "InvalidEmail": "Email is not in correct format!",
        "NotAuthorized": "You are not authorized User! Try again!",
        "InvalidTeamId": "Only alphanumeric and underscore are allowed with minimum 3 and maximum 15 characters!",
        "InvalidPassword": "Invalid password. Please match all password requirements!",
        "TeamIdError": "Please enter Team Id!"
    }
    message_title = {
        "UserExists": "User Already Exists",
        "InvalidPhone": "Invalid Phone Number",
        "InvalidEmail": "Invalid Email format",
        "NotAuthorized": "Not Authorized User",
        "InvalidTeamId": "Invalid Team Id",
        "InvalidPassword": "Invalid Password",
        "TeamIdError": "Team Id Error"
    }
    lambda_name = apis.api.get("get_teams")
    pl = {}
    response = make_lambda_call(lambda_name, pl, fetch_raw=True)
    print('teams :', response)
    request.session["existing_user"] = response["body"] if "body" in response else response
    if request.method == "GET":
        context["is_error"] = request.GET.get("is_error")
        print("IS REQUEST IS", context["is_error"])
        context["error"] = request.GET.get("error")
        if context["error"]:
            context['message'] = message_dict[context["error"]]
            context['message_title'] = message_title[context['error']]

    elif request.method == 'POST':
        try:
            pl = request.POST.dict()
            user_email = request.POST.get('user_email')
            if user_email:
                user_email = user_email.lower().strip()
            if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", user_email):
                return HttpResponseRedirect('../create_user?is_error=1&error=InvalidEmail')
            team_id = request.POST.get('team_id', "")
            if not team_id:
                return HttpResponseRedirect('../create_user?is_error=1&error=TeamIdError')
            if not re.match(r"^[a-zA-Z0-9_]*$", team_id) or len(team_id) < 3 or 20 < len(team_id):
                return HttpResponseRedirect('../create_user?is_error=1&error=InvalidTeamId')
            user_phone = request.POST.get('user_phone')
            country_code = request.POST.get('country_code')
            fub_crm_user = request.POST.get('fub_user')
            user_phone = f"+{country_code}{user_phone}"
            passcode = request.POST.get('user_password').strip()
            confirm_passcode = request.POST.get('user_confirm_password').strip()
            if passcode == passcode.lower() or passcode == passcode.upper() or re.findall('[^A-Za-z0-9]', passcode) == [] or len(passcode) < 8 or \
               passcode != confirm_passcode:
                return HttpResponseRedirect('../forgot_password?is_error=1&error=InvalidPassword')
            lambda_name = apis.api.get("register")

            pl = request.POST.dict()
            pl["user_phone"] = user_phone
            pl["user_email"] = user_email
            pl["fub_crm_user"] = fub_crm_user
            response = make_lambda_call(lambda_name, pl, fetch_raw=True)
            print("USER LOGIN RESP", response)

        except Exception as e:
            print("Exception Occured:", e)
            send_slack_notification_create_user(e, pl)

        if response.get("statusCode", 404) != 200:
            print("MESSAGE IN RESPONSE ", response['message'])
            if response['message']:

                traceback_string = response['message']
                print('traceback_string----', traceback_string, "----")
                if "UsernameExistsException" in traceback_string:
                    return HttpResponseRedirect('../create_user?is_error=1&error=UserExists')
                elif "InvalidParameterException" in traceback_string:
                    if "Invalid phone" in traceback_string:
                        return HttpResponseRedirect('../create_user?is_error=1&error=InvalidPhone')
                    elif "Invalid email" in traceback_string:
                        return HttpResponseRedirect('../create_user?is_error=1&error=InvalidEmail')
                elif "InvalidPasswordException" in traceback_string:
                    return HttpResponseRedirect('../create_user?is_error=1&error=InvalidPassword')
                elif "NotAuthorizedException" in traceback_string:
                    return HttpResponseRedirect('../create_user?is_error=1&error=NotAuthorized')
        else:
            request.session['team_id'] = request.POST.get('team_id', "")
            return HttpResponseRedirect('../verify_user?user_email=' + user_email)
    return render(request, 'dashboard/signup.html', context=context)


@csrf_exempt
def create_user_retool(request):
    # context = {}
    # message_dict = {
    #     "UserExists": "User with this email already exists!",
    #     "InvalidPhone": "Phone number is not in correct format!",
    #     "InvalidEmail": "Email is not in correct format!",
    #     "NotAuthorized": "You are not authorized User! Try again!",
    #     "InvalidTeamId": "Only alphanumeric and underscore are allowed",
    #     "InvalidPassword": "Invalid password. Please match all password requirements!",
    # }
    # message_title = {
    #     "UserExists": "User Already Exists",
    #     "InvalidPhone": "Invalid Phone Number",
    #     "InvalidEmail": "Invalid Email format",
    #     "NotAuthorized": "Not Authorized User",
    #     "InvalidTeamId": "Invalid Team Id",
    #     "InvalidPassword": "Invalid Password",
    # }
    lambda_name = apis.api.get("get_teams")
    pl = {}
    response = make_lambda_call(lambda_name, pl, fetch_raw=True)
    print('teams :', response)
    request.session["existing_user"] = response["body"] if "body" in response else response
    print("request.method", request.method)
    print("request.META", request.META)
    if request.method == 'POST':
        try:
            auth_code = request.META.get('HTTP_USER_AGENT')
            if 'Retool' not in auth_code:
                return JsonResponse({'message': 'Invalid Setting'})

            user_email = request.POST.get('user_email')
            if user_email:
                user_email = user_email.lower().strip()
            team_id = request.POST.get('team_id')
            if not re.match(r"^[a-zA-Z0-9_]*$", team_id):
                return JsonResponse({'message': 'InvalidTeamId'})
            user_phone = request.POST.get('user_phone')
            country_code = request.POST.get('country_code')
            fub_crm_user = request.POST.get('fub_user')
            user_phone = f"+{country_code}{user_phone}"

            lambda_name = apis.api.get("register")

            pl = request.POST.dict()
            pl["user_phone"] = user_phone
            pl["user_email"] = user_email
            pl["fub_crm_user"] = fub_crm_user
            response = make_lambda_call(lambda_name, pl, fetch_raw=True)
            print("USER LOGIN RESP", response)

        except Exception as e:
            send_slack_notification_create_user(e, pl, is_retool=True)

        if response.get("statusCode", 404) != 200:
            print("MESSAGE IN RESPONSE ", response['message'])
            if response['message']:
                traceback_string = response['message']
                print('traceback_string----', traceback_string, "----")
                if "UsernameExistsException" in traceback_string:
                    return JsonResponse({"statusCode": 404, 'message': 'UserExists'})
                elif "InvalidParameterException" in traceback_string:
                    if "Invalid phone" in traceback_string:
                        return JsonResponse({"statusCode": 404, 'message': 'InvalidPhone'})
                    elif "Invalid email" in traceback_string:
                        return JsonResponse({"statusCode": 404, 'message': 'InvalidEmail'})
                elif "InvalidPasswordException" in traceback_string:
                    return JsonResponse({"statusCode": 404, 'message': 'InvalidPassword'})
                elif "NotAuthorizedException" in traceback_string:
                    return JsonResponse({"statusCode": 404, 'message': 'NotAuthorized'})
        else:
            return JsonResponse({"statusCode": 200, 'message': 'User Created, They must Verify to signin'})


@require_http_methods(["GET", "POST"])
def login_user(request):
    context = {}
    message_dict = {
        "UserNotFoundException": "Please Register!",
        "NotAuthorizedException": "You are not authorized User! Please Register!",
        "InternalErrorException": "Sorry! There is some Internal Error! Please try again later",
        "PasswordResetRequiredException": "Try resetting the password",
        "TooManyRequestsException": "Try again later!",
        "UserNotConfirmedException": "You are not a confirmed user! Please register again!",
        "user_cancelled_login": "The user cancelled LinkedIn login",
        "UserPassError": "Invalid email or password. Please check your email and password",
        "user_cancelled_authorize": "The user refused to authorize the permissions request for the application.",
        "default": "Something went wrong. Please try again",
        "InvalidEmail": "Email is not in correct format!"
    }
    message_title = {
        "UserNotFoundException": "User Not Registered",
        "NotAuthorizedException": "User Not Authorized",
        "PasswordResetRequiredException": "Password Reset Required",
        "InternalErrorException": "Internal Error ",
        "TooManyRequestsException": "Too Many Requests",
        "UserNotConfirmedException": "User Not Confirmed",
        "user_cancelled_login": "User Cancelled Login",
        "user_cancelled_authorize": "User Cancelled to Authorize",
        "UserPassError": "Invalid email or password",
        "default": "Something went wrong. Please try again",
        "InvalidEmail": "Invalid Email format",
    }
    if request.method == "GET":
        if "email" in request.GET:
            context["email"] = request.GET.get("email")
        context["is_error"] = request.GET.get("is_error")
        context["error"] = request.GET.get("error")
        if context["error"]:
            context['message'] = message_dict.get(context["error"], message_dict["default"])
            context['message_title'] = message_title.get(context["error"], message_title["default"])

        return render(request, 'dashboard/login.html', context=context)

    elif request.method == "POST":
        lambda_name = apis.api.get("details")
        user_email = request.POST.get('user_email')
        if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", user_email):
            return HttpResponseRedirect('../login_user?is_error=1&error=InvalidEmail')
        print(dir(request.POST))
        pl = request.POST.dict()
        response = make_lambda_call(lambda_name, pl)
        response = response['body'] if 'body' in response else response
        print("Verify details", response)
        if "details" in response:
            if response.get('details') == "InternalErrorException":
                return HttpResponseRedirect('../login_user?is_error=1&error=InternalErrorException')
            elif response.get('details') == "InvalidLambdaResponseException":
                return HttpResponseRedirect('../login_user?is_error=1&error=InvalidLambdaResponseException')
            elif response.get('details') == "InvalidParameterException":
                return HttpResponseRedirect('../login_user?is_error=1&error=InvalidParameterException')
            elif response.get('details') == "NotAuthorizedException":
                return HttpResponseRedirect('../login_user?is_error=1&error=NotAuthorizedException')
            elif response.get('details') == "PasswordResetRequiredException":
                return HttpResponseRedirect('../login_user?is_error=1&error=PasswordResetRequiredException')
            elif response.get('details') == "ResourceNotFoundException":
                return HttpResponseRedirect('../login_user?is_error=1&error=ResourceNotFoundException')
            elif response.get('details') == "TooManyRequestsException":
                return HttpResponseRedirect('../login_user?is_error=1&error=TooManyRequestsException')
            elif response.get('details') == "UnexpectedLambdaException":
                return HttpResponseRedirect('../login_user?is_error=1&error=UnexpectedLambdaException')
            elif response.get('details') == "UserLambdaValidationException":
                return HttpResponseRedirect('../login_user?is_error=1&error=UserLambdaValidationException')
            elif response.get('details') == "UserNotConfirmedException":
                return HttpResponseRedirect('../verify_user?user_email=' + pl.get('user_email', ''))
            elif response.get('details') == "UserNotFoundException":
                return HttpResponseRedirect('../login_user?is_error=1&error=UserNotFoundException')
            else:
                return HttpResponseRedirect('../login_user?is_error=1&error=UserPassError')
        else:
            print("response from else ", response)
            response = response['body'] if 'body' in response else response
            request.session['is_loggedin'] = True
            request.session['AccessToken'] = response.get('AccessToken')
            request.session['RefreshToken'] = response.get('RefreshToken')
            request.session['IdToken'] = response.get('IdToken')
            request.session['ExpiresIn'] = response.get('ExpiresIn')
            request.session['team_id'] = response.get('team_id')
            request.session["first_name"] = response.get('first_name', "")
            request.session["last_name"] = response.get('last_name', "")
            request.session['user_name'] = response.get('first_name', "") + " " + response.get('last_name', "")
            request.session['user_email'] = response.get('email')
            request.session['timezone'] = response.get('user_timezone')
            request.session['phone'] = response.get('phone')
            request.session["organization_name"] = response.get("organization_name")
            request.session["planFubTwillio"] = response.get("planFubTwillio", False)
            request.session["embedded_form_type"] = response.get("embedded_form_type", "normal")
            request.session["planFubSisu"] = response.get("planFubSisu", False)
            request.session["planFubReport"] = response.get("planFubReport", False)
            request.session["smartlist_heatmap_report"] = response.get("smartlist_heatmap_report", False)
            request.session["planFubEmbeddedApp"] = response.get("planFubEmbeddedApp", False)
            request.session["AutomationBuilder"] = response.get("AutomationBuilder", False)
            request.session["FormBuilder"] = response.get("FormBuilder", False)
            request.session['heatmap_form_url'] = response.get("heatmap_form_url", "")
            request.session['subscription_status'] = response.get('status')
            request.session['end_date'] = response.get('end_date')
            request.session["planFubOtc"] = response.get("planFubOtc", False)
            request.session["chatgpt_integration"] = response.get("chatgpt_integration", False)
            request.session["planFubWufoo"] = response.get("planFubWufoo", False)

            if response.get('end_date', "2000-01-01") < datetime.datetime.now().strftime("%Y-%m-%d"):
                request.session['subscription_status'] = False
                return HttpResponseRedirect('../../payments/billing/')
            else:
                request.session['subscription_status'] = True
            return HttpResponseRedirect('../../user/credential_form')


@require_http_methods(["GET", "POST"])
def verify_user(request):
    if request.method == "GET":
        user_email = request.GET.get('email', "").replace(' ', '+')
        otp = request.GET.get('otp', "")
        context = {}
        context["is_error"] = False
        if "otp" in request.GET:
            context["otp_code"] = request.GET.get("otp")
            context["has_code"] = True
        else:
            context["has_code"] = False
        if user_email and otp:
            lambda_name = apis.api.get("verify")
            pl = {"user_email": user_email, "user_code": otp}
            response = make_lambda_call(lambda_name, pl, fetch_raw=True)
            encoded_user_email = urllib.parse.quote(user_email.encode('utf8'))
            if response.get("statusCode", 404) == 200:
                return HttpResponseRedirect(f'login_user?email={encoded_user_email}&verified=true', context)
            elif "CONFIRMED" in response.get("details"):
                return HttpResponseRedirect(f'login_user?email={encoded_user_email}&verified=true', context)
            else:
                context['user_email'] = encoded_user_email
                context['is_error'] = 2
                return render(request, 'dashboard/verify.html', context)
        team_id = request.session.get('team_id', "")
        print("TEAM ID in VERIFY EMAIL:", team_id)
        return render(request, 'dashboard/verify.html',
                      {"user_email": user_email, "otp": otp, "team_id": team_id})
    if request.method == 'POST':
        user_email = request.POST['user_email'].replace(' ', '+')
        user_code = int(request.POST['user_code'])
        print('verify_user:', user_email, user_code)
        lambda_name = apis.api.get("verify")
        print(dir(request.POST))
        pl = request.POST.dict()
        response = make_lambda_call(lambda_name, pl, fetch_raw=True)
        print('verify_user:', response)
        if response.get("statusCode", 404) == 200:
            return HttpResponseRedirect('login_user')
        elif "CONFIRMED" in response.get("details"):
            return HttpResponseRedirect('login_user')
        else:
            return render(request, 'dashboard/verify.html',
                          {"user_email": user_email, "is_error": 2})


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('../login_user')


def check_team(request):
    team_id = request.GET.get("team", "")
    exis_data = request.session.get("existing_user", {})
    if team_id not in exis_data.get("team_id", ""):
        return JsonResponse({"status": True})
    else:
        return JsonResponse({"status": False})


def check_email(request):
    email = request.GET.get("email", "").strip()
    exis_data = request.session.get("existing_user", {})
    if email not in exis_data.get("email", ""):
        return JsonResponse({"status": True})
    else:
        return JsonResponse({"status": False})


@require_http_methods(["GET", "POST"])
def send_confirmation_code(request):
    """
        This view if used for forget password API
    """
    context = {}
    message_dict = {
        "ResourceNotFoundException": "User Not Found! Please Register!",
        "CodeDeliveryFailureException": "Sorry! There is some Internal Error! Please try again later",
        "UserNotFoundException": "Please Register!",
        "InvalidParameterException": "Sorry! There is some Internal Error! Please try again later",
        "NotAuthorizedException": "You are not authorized User! Please Register!",
        "InternalErrorException": "Sorry! There is some Internal Error! Please try again later",
        "PasswordResetRequiredException": "Try resetting the password",
        "TooManyRequestsException": "Try again later!",
        "UserNotConfirmedException": "You are not a confirmed user! Please register again!",
        "user_cancelled_login": "The user cancelled LinkedIn login",
        "UserPassError": "Invalid email or password. Please check your email and password",
        "user_cancelled_authorize": "The user refused to authorize the permissions request for the application.",
        "InvalidEmail": "Email is not in correct format!",
    }
    message_title = {
        "ResourceNotFoundException": "User Not Found",
        "InvalidParameterException": "Invalid Parameter",
        "CodeDeliveryFailureException": "Code Delivery Failed",
        "UserNotFoundException": "User Not Registered",
        "NotAuthorizedException": "User Not Authorized",
        "PasswordResetRequiredException": "Password Reset Required",
        "InternalErrorException": "Internal Error ",
        "TooManyRequestsException": "Too Many Requests",
        "UserNotConfirmedException": "User Not Confirmed",
        "user_cancelled_login": "User Cancelled Login",
        "user_cancelled_authorize": "User Cancelled to Authorize",
        "UserPassError": "Invalid email or password",
        "InvalidEmail": "Invalid Email format"
    }
    if request.method == 'GET':
        print("IN_GET")
        if "is_error" in request.GET:
            context["is_error"] = request.GET.get("is_error", 0)
            context["error"] = request.GET.get("error")
            if context["error"]:
                context['message'] = message_dict[context["error"]]
                context['message_title'] = message_title[context['error']]
            return render(request, 'dashboard/send_confirmation_code.html', context=context)
    elif request.method == 'POST':
        email = request.POST.get('user_email').strip()
        if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=InvalidEmail')
        lambda_name = apis.api.get("send_confirmation_code")
        pl = {'user_email': email}
        response = make_lambda_call(lambda_name, pl, fetch_raw=True)
        print('sendCode API response: ', response)
        if response.get("statusCode", 404) != 200:
            if "details" in response:
                if response.get('details') == "CodeDeliveryFailureException":
                    return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=CodeDeliveryFailureException')
                elif response.get('details') == "InternalErrorException":
                    return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=InternalErrorException')
                elif response.get('details') == "InvalidParameterException":
                    return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=InvalidParameterException')
                elif response.get('details') == "NotAuthorizedException":
                    return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=NotAuthorizedException')
                elif response.get('details') == "ResourceNotFoundException":
                    return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=ResourceNotFoundException')
                elif response.get('details') == "TooManyRequestsException":
                    return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=TooManyRequestsException')
                elif response.get('details') == "UserNotConfirmedException":
                    return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=UserNotConfirmedException')
                elif response.get('details') == "UserNotFoundException":
                    return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=UserNotFoundException')
                else:
                    return HttpResponseRedirect('../send_confirmation_code?is_error=1&error=UserNotFoundException')
        return HttpResponseRedirect('../forgot_password?email=' + email)
    return render(request, 'dashboard/send_confirmation_code.html')


@require_http_methods(["GET", "POST"])
def forgot_password(request):
    context = {}
    message_dict = {
        "ResourceNotFoundException": "User Not Found! Please Register!",
        "CodeDeliveryFailureException": "Sorry! There is some Internal Error! Please try again later",
        "UserNotFoundException": "Please Register!",
        "InvalidParameterException": "Sorry! There is some Internal Error! Please try again later",
        "NotAuthorizedException": "You are not authorized User! Please Register!",
        "InternalErrorException": "Sorry! There is some Internal Error! Please try again later",
        "PasswordResetRequiredException": "Try resetting the password",
        "TooManyRequestsException": "Try again later!",
        "UserNotConfirmedException": "You are not a confirmed user! Please register again!",
        "user_cancelled_login": "The user cancelled LinkedIn login",
        "UserPassError": "Invalid email or password. Please check your email and password",
        "user_cancelled_authorize": "The user refused to authorize the permissions request for the application.",
        "LimitExceededException": "Please try again after some time.",
        "InvalidPassword": "Invalid password. Please match all password requirements!"
    }
    message_title = {
        "ResourceNotFoundException": "User Not Found",
        "InvalidParameterException": "Invalid Parameter",
        "CodeDeliveryFailureException": "Code Delivery Failed",
        "UserNotFoundException": "User Not Registered",
        "NotAuthorizedException": "User Not Authorized",
        "PasswordResetRequiredException": "Password Reset Required",
        "InternalErrorException": "Internal Error ",
        "TooManyRequestsException": "Too Many Requests",
        "UserNotConfirmedException": "User Not Confirmed",
        "user_cancelled_login": "User Cancelled Login",
        "user_cancelled_authorize": "User Cancelled to Authorize",
        "UserPassError": "Invalid email or password",
        "LimitExceededException": "Attempts Exhausted",
        "InvalidPassword": "Invalid Password"
    }

    context["is_error"] = False
    if request.method == 'GET':
        if "email" in request.GET:
            context["email"] = request.GET.get("email").replace(' ', '+')
        if "otp" in request.GET:
            context["otp_code"] = request.GET.get("otp")
            context["has_code"] = True
        else:
            context["has_code"] = False
        if "is_error" in request.GET:
            context["is_error"] = request.GET.get("is_error", 0)
            context["error"] = request.GET.get("error")
            if context["error"]:
                context['message'] = message_dict[context["error"]]
                context['message_title'] = message_title[context['error']]
            return render(request, 'dashboard/forgot_password.html', context=context)
    elif request.method == 'POST':
        email = request.POST.get('user_email').strip().replace(' ', '+')
        encoded_email = urllib.parse.quote(email.encode('utf8'))
        otp = request.POST.get('otp').strip()
        passcode = request.POST.get('new_password').strip()
        confirm_passcode = request.POST.get('user_confirm_password').strip()
        if passcode == passcode.lower() or passcode == passcode.upper() or re.findall('[^A-Za-z0-9]', passcode) == [] or len(passcode) < 8 or \
           passcode != confirm_passcode:
            return HttpResponseRedirect('../forgot_password?is_error=1&error=InvalidPassword')
        lambda_name = apis.api.get("forgot_password")
        pl = {'user_email': email, "otp": otp, "passcode": passcode, "confirm_passcode": confirm_passcode}
        response = make_lambda_call(lambda_name, pl, fetch_raw=True)
        print('forgot_password_API_response: ', response)
        if response.get("statusCode", 404) != 200:
            if "details" in response:
                if response.get('details') == "CodeDeliveryFailureException":
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=CodeDeliveryFailureException')
                elif response.get('details') == "InternalErrorException":
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=InternalErrorException')
                elif response.get('details') == "InvalidParameterException":
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=InvalidParameterException')
                elif response.get('details') == "NotAuthorizedException":
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=NotAuthorizedException')
                elif response.get('details') == "ResourceNotFoundException":
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=ResourceNotFoundException')
                elif response.get('details') == "TooManyRequestsException":
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=TooManyRequestsException')
                elif response.get('details') == "UserNotConfirmedException":
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=UserNotConfirmedException')
                elif response.get('details') == "UserNotFoundException":
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=UserNotFoundException')
                elif response.get('details') == "LimitExceededException":
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=LimitExceededException')
                else:
                    return HttpResponseRedirect('../forgot_password?is_error=1&error=InternalErrorException')
        return HttpResponseRedirect('../login_user?email=' + encoded_email)
    return render(request, 'dashboard/forgot_password.html', context=context)
