import requests
import time

# Set up your Follow Up Boss API key
API_KEY = 'YOUR_API_KEY'

# Function to get contacts from Follow Up Boss
def get_contacts(page):
    url = f'https://api.followupboss.com/v1/people?page={page}'
    headers = {
        'Authorization': f'Basic {API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 429:
        print("Rate limit reached, sleeping for 60 seconds...")
        time.sleep(60)
        return get_contacts(page)
    
    return response.json()

# Function to update a contact's feedbackForm field
def update_contact(contact_id, showings_feedback_form, booking_call_feedback_form):
    url = f'https://api.followupboss.com/v1/people/{contact_id}'
    headers = {
        'Authorization': f'Basic {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'custom': {
            'feedbackForm': f'{showings_feedback_form} {booking_call_feedback_form}'
        }
    }
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 429:
        print(f"Rate limit reached while updating contact {contact_id}, sleeping for 60 seconds...")
        time.sleep(60)
        return update_contact(contact_id, showings_feedback_form, booking_call_feedback_form)
    
    return response.json()

# Fetch all contacts and update feedbackForm only if empty
page = 1
contacts_updated = 0

while True:
    contacts = get_contacts(page)
    if not contacts['people']:
        break
    
    for person in contacts['people']:
        contact_id = person['id']
        fub_lead_id = person['id']
        
        if 'custom' in person and 'feedbackForm' in person['custom'] and not person['custom']['feedbackForm']:
            showings_feedback_form = f'https://datahelp.wufoo.com/forms/ewrwer&field19={fub_lead_id}'
            booking_call_feedback_form = f'https://datahelp.wufoo.com/forms/wr&field9={fub_lead_id}'
            
            update_contact(contact_id, showings_feedback_form, booking_call_feedback_form)
            contacts_updated += 1
    
    page += 1

print(f'{contacts_updated} contacts updated successfully.')
