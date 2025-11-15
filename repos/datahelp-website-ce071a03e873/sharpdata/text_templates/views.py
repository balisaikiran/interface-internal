from django.shortcuts import render
from django.http import HttpResponseRedirect
from sharpdata.helper import make_lambda_call, login_check_decorator
from . import apis


@login_check_decorator
def text_templates(request):
    context = {}
    context = {}
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    if request.method == "GET":
        # fetch all the tags
        lambda_name = apis.api["list_templates"]
        pl = {"team_id": request.session.get("team_id")}
        resp = make_lambda_call(lambda_name, pl)
        resp = resp['body'] if 'body' in resp else resp
        context["message_list"] = resp["results"]
    return render(request, 'dashboard/text_templates.html', context=context)


@login_check_decorator
def edit_text_templates(request):
    context = {}
    context = {}
    context["planFubTwillio"] = request.session["planFubTwillio"]
    context["planFubSisu"] = request.session["planFubSisu"]
    context["smartlist_heatmap_report"] = request.session["smartlist_heatmap_report"]
    context["planFubEmbeddedApp"] = request.session.get("planFubEmbeddedApp", False)
    if request.method == "GET":
        pl = {}
        pl["did"] = request.GET.get("id")
        lambda_name = apis.api["get_template"]
        resp = make_lambda_call(lambda_name, pl)
        resp = resp['body'] if 'body' in resp else resp
        if resp["statusCode"] == 200:
            context["result"] = resp["result"]
    elif request.method == "POST":
        print(request.POST.dict())
        req = request.POST.dict()
        pl = {}
        pl["did"] = req.get("update_id")
        pl["tag_name"] = req.get("tag_name")
        pl["text_message"] = req.get("text_message")
        pl["custom_field_name"] = req.get("custom_field_name")
        pl["team_id"] = request.session.get("team_id")
        if req.get("update_id", "") == "":

            lambda_name = apis.api["create_template"]
        else:
            lambda_name = apis.api["update_template"]

        resp = make_lambda_call(lambda_name, pl)
        resp = resp['body'] if 'body' in resp else resp
        return HttpResponseRedirect("../text-templates")
    return render(request, 'dashboard/create_text_template.html', context=context)


@login_check_decorator
def delete_text_template(request):
    if request.method == "GET":
        pl = {}
        pl["did"] = request.GET.get("id")
        lambda_name = apis.api["delete_template"]
        make_lambda_call(lambda_name, pl)
    return HttpResponseRedirect("/user/text-templates")
