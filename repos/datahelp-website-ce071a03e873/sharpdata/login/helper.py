'''
    Author: Saurav Panda
    Co-Author :


    Description : This file Functions to work with API's
'''

import requests
import json


def session_detials(request, context):
    login = False
    if 'is_loggedin' in request.session:
        if request.session['is_loggedin'] is True:
            login = True
            context['username'] = request.session['name']
            context['email'] = request.session['email']
            context['country'] = request.session['country']
            context['team_id'] = request.session['team_id']
            context['login'] = login
    return context


def make_api_call(url, payload, fetch_raw=False):
    '''
        This function is used to make api calls.
        Input : url - api url to be called
                payload - payload to be posted to API
        Output: event - API response in json format
    '''

    # Define the authorization header
    headers = {
        'Authorization': "Bearer 2HIyxc6MWp8022VdL1jqc8MCqF1R2t6h4dfGNhSX",
    }

    # Make a post request
    print("pl : ", payload)
    response = requests.request("POST", url, json=payload, headers=headers)
    print("Event raw txt: ", response.text)
    event = json.loads(response.text)
    if not fetch_raw:
        if 'body' in event:
            print("getting body")
            event = event["body"]
        if isinstance(type(event), type("a")):
            print("loading string")
            event = json.loads(event)
    return event
