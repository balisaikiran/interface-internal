import requests

# Set up your Follow Up Boss API key
API_KEY = 'fka_1efHhLHOvvrDo79BhaeAm2vsv0Ddy2gxIv'

# Function to get a single contact's details by ID
def get_contact(contact_id):
    url = f'https://bradysandahl.followupboss.com/people/{contact_id}'
    headers = {
        'Authorization': f'Basic {API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Test with a single contact ID (replace with an actual contact ID from your FUB)
contact_id = '99554'

contact = get_contact(contact_id)

# Print the contact's field names
if 'people' in contact:
    person = contact['people']
    print("Fields for contact ID:", contact_id)
    for key in person.keys():
        print(f"{key}: {person[key]}")
else:
    print("Contact not found or error in API call.")
