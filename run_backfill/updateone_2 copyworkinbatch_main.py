import requests
from requests.auth import HTTPBasicAuth

API_KEY = 'fka_1efHhLHOvvrDo79BhaeAm2vsv0Ddy2gxIv'

def get_contacts(page):
    url = 'https://api.followupboss.com/v1/people?sort=id'
    params = {'limit': 100, 'offset': 3000}
    auth = HTTPBasicAuth(API_KEY, '')
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code == 200:
        return response.json().get('people', [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

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
    page = 0
    while True:
        contacts = get_contacts(page)
        if not contacts:
            break
        
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
        
        page += 1

# Run the update process
populate_custom_fields_for_contacts()