import json

with open('input.json') as f:
    data = json.load(f)

# Filter out unwanted fields
filtered_data = [{'city': item['city'], 'state_id': item['state_id'], 'state_name': item['state_name']} for item in data]

# Output the modified JSON
with open('output.json', 'w') as f:
    json.dump(filtered_data, f, indent=4)