import requests
from requests.auth import HTTPBasicAuth
import time
import os
API_KEY = 'fka_1efHhLHOvvrDo79BhaeAm2vsv0Ddy2gxIv'
BATCH_SIZE = 100  # Number of contacts to fetch per request
SLEEP_TIME = 1    # Time to wait between requests to avoid hitting rate limits
LAST_UPDATED_CONTACT_ID_FILE = 'last_updated_contact_id.txt'
START_CONTACT_ID = 29000  # Contact ID to start processing from
def get_contacts(next_link=None):
    url = next_link if next_link else 'https://api.followupboss.com/v1/people'
    params = {'limit': BATCH_SIZE, 'offset': 0} if not next_link else None
    auth = HTTPBasicAuth(API_KEY, '')
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, auth=auth, params=params)
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

def process_contacts():
    last_updated_contact_id = read_last_updated_contact_id()
    next_link = None
    total_updated = 0

    while True:
        data = get_contacts(next_link)
        if not data or 'people' not in data:
            break
        
        contacts = data['people']
        for contact in contacts:
            contact_id = contact['id']

            if contact_id <= last_updated_contact_id:
                continue  # Skip this contact

            custom_fields = contact.get('custom', {})

            # Check if the custom fields are empty
            if not custom_fields.get('customBookingCallFeedbackForm') and not custom_fields.get('customShowingsFeedbackForm'):
                update_data = {
                    'customBookingCallFeedbackForm': f'https://datahelp.wufoo.com/forms/z2c3m8t1rz47gt&field9={contact_id}',
                    'customShowingsFeedbackForm': f'https://datahelp.wufoo.com/forms/zb41peu1vmhyzd&field19={contact_id}'
                }
                updated_contact = update_contact(contact_id, update_data)
                if updated_contact:
                    total_updated += 1
                    print(f"Successfully updated contact ID: {contact_id}")
                    last_updated_contact_id = contact_id
                else:
                    print(f"Failed to update contact ID: {contact_id}")

        # Check for nextLink for the next batch of contacts
        next_link = data.get('nextLink')
        if not next_link:
            break

        # Sleep to avoid hitting rate limits
        time.sleep(SLEEP_TIME)

    write_last_updated_contact_id(last_updated_contact_id)
    print(f"Total contacts updated: {total_updated}")

def read_last_updated_contact_id():
    if os.path.exists(LAST_UPDATED_CONTACT_ID_FILE):
        with open(LAST_UPDATED_CONTACT_ID_FILE, 'r') as f:
            return int(f.read())
    else:
        return 0

def write_last_updated_contact_id(contact_id):
    with open(LAST_UPDATED_CONTACT_ID_FILE, 'w') as f:
        f.write(str(contact_id))

# Run the update process
process_contacts()