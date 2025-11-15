import requests
from requests.auth import HTTPBasicAuth

API_KEY = 'fka_1efHhLHOvvrDo79BhaeAm2vsv0Ddy2gxIv'

def get_contact(contact_id):
    url = f'https://api.followupboss.com/v1/people/{contact_id}'
    params = {'fields': 'allFields'}
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

# Test with a single contact ID (replace with an actual contact ID from your FUB)
contact_id = '99554'

contact = get_contact(contact_id)

# Update fields if contact is found
if contact:
    print("Fields for contact ID:", contact_id)
    for key, value in contact.items():
        if key == 'custom' and isinstance(value, dict):
            print("Custom Fields:")
            for custom_key, custom_value in value.items():
                print(f"  {custom_key}: {custom_value}")
        else:
            print(f"{key}: {value}")

    # Check existing custom fields
    if 'custom' in contact and isinstance(contact['custom'], dict):
        # Update URLs
        update_data = {
            # 'custom': {
                'customBookingCallFeedbackForm': f'https://datahelp.wufoo.com/forms/z2c3m8t1rz47gt&field9={contact_id}',
                'customShowingsFeedbackForm': f'https://datahelp.wufoo.com/forms/zb41peu1vmhyzd&field19={contact_id}'
            # }
        }
        updated_contact = update_contact(contact_id, update_data)

        if updated_contact:
            print("Updated contact data:")
            for key, value in updated_contact.items():
                if key == 'custom' and isinstance(value, dict):
                    print("Custom Fields:")
                    for custom_key, custom_value in value.items():
                        print(f"  {custom_key}: {custom_value}")
                else:
                    print(f"{key}: {value}")
        else:
            print("Error updating contact.")
    else:
        print("No custom fields found.")
else:
    print("Contact not found or error in API call.")
