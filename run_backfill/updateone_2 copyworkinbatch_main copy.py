import requests
from requests.auth import HTTPBasicAuth

API_KEY = 'fka_1efHhLHOvvrDo79BhaeAm2vsv0Ddy2gxIv'

def get_contacts(url):
    auth = HTTPBasicAuth(API_KEY, '')
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
        data = response.json()
        return data.get('people', []), data.get('nextLink')
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return [], None

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

def populate_custom_fields_for_contacts(start_url):
    url = start_url
    while url:
        contacts, next_link = get_contacts(url)
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

        # Move to the next page using nextLink URL
        url = next_link

# Start URL for pagination, adjust as per your needs
start_url = 'https://api.followupboss.com/v1/people?sort=id'
populate_custom_fields_for_contacts(start_url)