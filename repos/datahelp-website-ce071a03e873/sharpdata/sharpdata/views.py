import traceback

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import requests
import json

try:
    f = open("/var/www/config", "r")
    data = json.loads(f.read())
    f.close()
    STAGE = data.get('STAGE', 'dev')
except Exception as e:
    print(e)
    STAGE = "dev"


def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    if STAGE == 'prod':
        url = "https://hooks.slack.com/services/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"
    else:
        url = "https://hooks.slack.com/services/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"

    pl = {"text": f"*404 Error occured*\n ENV : `{STAGE}`\
        \nPATH_INFO: `{request.META['PATH_INFO']}`, \nmethod: `{request.META['REQUEST_METHOD']}`,\
        \nQUERY_STRING: `{request.META['QUERY_STRING']}` \nREMOTE_ADDR: `{request.META['REMOTE_ADDR']}`"}
    print("404 error Request meta", request.META)
    try:
        requests.post(url, json=pl)
    except Exception:
        print(traceback.format_exc())
        pass
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    # if STAGE == 'prod':
    #     url = "https://hooks.slack.com/services/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"
    # else:
    url = "https://hooks.slack.com/services/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"

    pl = {
        "text": f"*500 Error occured*\n ENV : `{STAGE}`\
            \nPATH_INFO: `{request.META['PATH_INFO']}`, \nmethod: `{request.META['REQUEST_METHOD']}`,\
            \nQUERY_STRING: `{request.META['QUERY_STRING']}` \nREMOTE_ADDR: `{request.META['REMOTE_ADDR']}`"}
    print("500 error Request meta", request.META)
    try:
        requests.post(url, json=pl)
    except Exception:
        print(traceback.format_exc())
        pass

    return response


def calendly(request, id):
    print(request.GET)
    pl = dict(request.GET)
    if 'invitee_full_name' in pl:
        username = pl['invitee_full_name'][0]

        firstname = username.split(' ')[0]
        lastname = username.split(' ')[1]
    else:
        firstname = pl['invitee_first_name'][0]
        lastname = pl['invitee_last_name'][0]
    invitee_email = pl['invitee_email'][0]

    form_url = f"https://datahelp.wufoo.com/forms/{id}?Field211={firstname}&Field212={lastname}&Field209={invitee_email}"
    return HttpResponseRedirect(form_url)


def health_check(request):
    return JsonResponse({'status': 200})


def test_resp(request):
    return JsonResponse({'status': 200, 'message': "Test!!"})
