import requests
from requests.auth import HTTPBasicAuth

# Set up your Follow Up Boss API key
API_KEY = 'fka_1efHhLHOvvrDo79BhaeAm2vsv0Ddy2gxIv'

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
        if 'customfields' in data:
            return data['customfields']
        else:
            print(f"No 'customfields' key found in API response:")
            print(data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching custom fields: {e}")
        return None

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

def fetch_custom_field_values(contact_id):
    url = f'https://api.followupboss.com/v1/people/{contact_id}/customFieldValues'
    auth = HTTPBasicAuth(API_KEY, '')
    headers = {
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()
        if 'customFieldValues' in data:
            return data['customFieldValues']
        else:
            print(f"No 'customFieldValues' key found in API response:")
            print(data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching custom field values: {e}")
        return None

def print_custom_fields(contact, custom_fields, custom_field_values):
    if 'custom' in contact and isinstance(contact['custom'], dict):
        print("Custom Fields for contact:")
        for custom_field_value in custom_field_values:
            custom_field_id = custom_field_value['customFieldId']
            custom_field_name = next((cf['name'] for cf in custom_fields if cf['id'] == custom_field_id), f"Custom Field ID {custom_field_id}")
            print(f"  {custom_field_name}: {custom_field_value['value']}")
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
        # Fetch custom field values
        custom_field_values = fetch_custom_field_values(contact_id)

        if custom_field_values:
            print(f"Custom fields for contact ID {contact_id}:")
            print_custom_fields(contact, custom_fields, custom_field_values)
        else:
            print("Failed to fetch custom field values.")
    else:
        print("Contact not found or error in fetching contact details.")
else:
    print("Failed to fetch custom fields. Check API key and permissions.")