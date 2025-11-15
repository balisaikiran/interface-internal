import requests
from requests.auth import HTTPBasicAuth

# Set up your Follow Up Boss API key
API_KEY = 'fka_1efHhLHOvvrDo79BhaeAm2vsv0Ddy2gxIv'

# Function to fetch custom fields from Follow Up Boss
def fetch_custom_fields():
    url = 'https://api.followupboss.com/v1/customFields'
    auth = HTTPBasicAuth(API_KEY, '')
    headers = {
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()
        if 'items' in data:
            return data['items']
        else:
            print(f"No 'items' key found in API response:")
            print(data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching custom fields: {e}")
        return None

# Function to get a single contact's details by ID
def get_contact(contact_id):
    url = f'https://api.followupboss.com/v1/people/{contact_id}'
    auth = HTTPBasicAuth(API_KEY, '')
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching contact details: {e}")
        return None

# Function to print custom fields for a contact
def print_custom_fields(contact, custom_fields):
    if 'custom' in contact and isinstance(contact['custom'], dict):
        print("Custom Fields for contact:")
        for key, value in contact['custom'].items():
            # Find the custom field name using custom field ID
            custom_field_name = next((cf['name'] for cf in custom_fields if cf['id'] == key), f"Custom Field ID {key}")
            print(f"  {custom_field_name}: {value}")
    else:
        print("No custom fields found for this contact.")

# Test with a single contact ID (replace with an actual contact ID from your FUB)
contact_id = '101709'

# Fetch custom fields first
custom_fields = fetch_custom_fields()

if custom_fields:
    # Now fetch the contact details
    contact = get_contact(contact_id)

    if contact:
        print(f"Custom fields for contact ID {contact_id}:")
        print_custom_fields(contact, custom_fields)
    else:
        print("Contact not found or error in fetching contact details.")
else:
    print("Failed to fetch custom fields. Check API key and permissions.")