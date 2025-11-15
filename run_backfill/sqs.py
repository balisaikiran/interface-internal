import boto3
import json
import hashlib

# Create SQS client
sqs = boto3.client('sqs')

# URL of the SQS queue
queue_url = 'https://sqs.us-west-2.amazonaws.com/917092476223/backfillSQLtest.fifo'

def send_message(fub_id, fub_person_id):
    message_body = {
        'fub_id': fub_id,
        'fub_person_id': fub_person_id
    }

    # Create a deduplication ID using the content of the message
    message_deduplication_id = hashlib.md5(json.dumps(message_body).encode('utf-8')).hexdigest()

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message_body),
        MessageGroupId='default',  # Required for FIFO queues
        MessageDeduplicationId=message_deduplication_id  # Prevents duplicates
    )

    print(f"Message ID: {response['MessageId']}")

# Example usage
send_message('example_fub_id', 'example_fub_person_id')
