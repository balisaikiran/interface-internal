import requests
from requests.auth import HTTPBasicAuth
import json
import os

API_KEY = 'fka_1efHhLHOvvrDo79BhaeAm2vsv0Ddy2gxIv'
STATE_FILE = 'pagination_state.json'

def save_state(next_link, page_number):
    with open(STATE_FILE, 'w') as file:
        json.dump({'nextLink': next_link, 'page_number': page_number}, file)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as file:
            state = json.load(file)
            return state.get('nextLink', None), state.get('page_number', 0)
    return None, 0

def get_contacts(next_link=None):
    url = next_link if next_link else 'https://api.followupboss.com/v1/people?sort=id&limit=100&offset=1900'
    auth = HTTPBasicAuth(API_KEY, '')
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def update_contact(contact_id, update_data):
    url = f'https://api.followupboss.com/v1/people/{contact_id}'
    auth = HTTPBasicAuth(API_KEY, '')
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, auth=auth, json=update_data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def populate_custom_fields_for_contacts():
    next_link, page_number = load_state()
    while True:
        response_data = get_contacts(next_link)
        if not response_data or 'people' not in response_data:
            break

        contacts = response_data['people']
        next_link = response_data.get('nextLink')
        save_state(next_link, page_number)

        for contact in contacts:
            contact_id = contact['id']
            custom_fields = contact.get('custom', {})

            # Check if the custom fields are empty
            if not custom_fields.get('customBookingCallFeedbackForm') and not custom_fields.get('customShowingsFeedbackForm'):
                update_data = {
                    'customBookingCallFeedbackForm': f'https://datahelp.wufoo.com/forms/z2c3m8t1rz47gt&field9={contact_id}',
                    'customShowingsFeedbackForm': f'https://datahelp.wufoo.com/forms/zb41peu1vmhyzd&field19={contact_id}'
                }
                updated_contact = update_contact(contact_id, update_data)
                if updated_contact:
                    print(f"Successfully updated contact ID: {contact_id}")
                else:
                    print(f"Failed to update contact ID: {contact_id}")

        page_number += 1
        if not next_link:
            break

# Run the update process
populate_custom_fields_for_contacts()
