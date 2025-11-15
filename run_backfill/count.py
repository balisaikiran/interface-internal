import requests
from requests.auth import HTTPBasicAuth

API_KEY = 'fka_1efHhLHOvvrDo79BhaeAm2vsv0Ddy2gxIv'

def get_contacts(page, fields='allFields'):
    url = 'https://api.followupboss.com/v1/people?sort=id'
    params = {'limit': 100, 'offset': page * 100, 'fields': fields}
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
    params = {'fields': 'allFields'}
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, auth=auth,params=params, json=update_data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def fetch_and_filter_contacts():
    page = 0
    contacts_to_update = []
    while True:
        contacts = get_contacts(page)
        if not contacts:
            break
        
        for contact in contacts:
            custom_fields = contact.get('custom', {})
            if not custom_fields.get('customBookingCallFeedbackForm') and not custom_fields.get('customShowingsFeedbackForm'):
                contacts_to_update.append(contact)
        
        page += 1
        print(f"Fetched page {page}, total contacts to update: {len(contacts_to_update)}")
    
    return contacts_to_update

def update_contacts_in_batches(contacts, batch_size=100):
    for i in range(0, len(contacts), batch_size):
        batch = contacts[i:i + batch_size]
        for contact in batch:
            contact_id = contact['id']
            update_data = {
                'customBookingCallFeedbackForm': f'https://datahelp.wufoo.com/forms/z2c3m8t1rz47gt&field9={contact_id}',
                'customShowingsFeedbackForm': f'https://datahelp.wufoo.com/forms/zb41peu1vmhyzd&field19={contact_id}'
            }
            updated_contact = update_contact(contact_id, update_data)
            if updated_contact:
                print(f"Successfully updated contact ID: {contact_id}")
            else:
                print(f"Failed to update contact ID: {contact_id}")

# Fetch and filter contacts
contacts_to_update = fetch_and_filter_contacts()

# Update contacts in batches
update_contacts_in_batches(contacts_to_update, batch_size=100)