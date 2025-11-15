import boto3
import time
client = boto3.client('dynamodb')

response = client.list_tables(
    Limit=100
)
for table in response['TableNames']:
    print(table)
    response = client.create_backup(
        TableName=table,
        BackupName='migration-backup-010522-' + table
    )
    time.sleep(0.2)
