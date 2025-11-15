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

# Test with a single contact ID (replace with an actual contact ID from your FUB)
contact_id = '101709'

contact = get_contact(contact_id)

# Print the contact's field names and values
if contact:
    print("Fields for contact ID:", contact_id)
    for key, value in contact.items():
        if key == 'custom' and isinstance(value, dict):
            print("Custom Fields:")
            for custom_key, custom_value in value.items():
                print(f"  {custom_key}: {custom_value}")
        else:
            print(f"{key}: {value}")
else:
    print("Contact not found or error in API call.")