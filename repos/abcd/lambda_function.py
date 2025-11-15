import boto3
import psycopg2

dynamodb = boto3.resource('dynamodb')
table_name = 'fub-dev-env-recruiterOpportunityTable-13PEXPTQDTLRX'

def get_postgres_config():
    # Replace with your own Postgres config
    postgres_config = {
        'user': 'postgres_user',
        'password': 'Dev#test#23',
        'host': 'dev-database-2.cmbltiirvdvj.us-west-2.rds.amazonaws.com',
        'port': 5432,
        'database': 'postgres_user'
    }
    return postgres_config

def sync_data():
    postgres_config = get_postgres_config()
    conn = psycopg2.connect(**postgres_config)
    cur = conn.cursor()

    # Sync data from DynamoDB to Postgres
    table = dynamodb.Table(table_name)
    dynamodb_data = table.scan()
    postgres_data = []
    for item in dynamodb_data['Items']:
        postgres_item = {}
        common_columns = [
            'isu_client_updated_ts',
            'opp_updated_ts',
            'opp_stage',
            'fub_deal_created_ts',
            'opp_type',
            'opp_appt_date',
            'fub_deal_stage_name',
            'opp_appt_met_date',
            'fub_person_id',
            'opp_price',
            'isu_client_created_ts',
            'opp_created_ts',
            'fub_deal_id',
            'opp_appt_disposition',
            'teamfubdealid',
            'team',
            'fub_deal_entered_stage_ts',
            'isu_client_id',
            'opp_assigned_osa',
            'opp_isa',
            'opp_notes',
            'opp_address',
            'opp_agreement_expiration_date',
            'appt_set_entry_id',
            'fub_appt_start_time',
            'opp_commission_percent',
            'fub_original_appt_start_time',
            'disp_text_wait_timestamp',
            'appt_set_lead_type',
            'appt_set_platform',
            'disp_text_original_wait_timestamp',
            'opp_address2',
            'opp_city',
            'opp_postal_code',
            'opp_last_name',
            'opp_state',
            'previous_opp_stage',
            'createentryid',
            'createformid'
        ]
        for column in common_columns:
            postgres_item[column] = item[column]['S']
        postgres_data.append(postgres_item)
    cur.executemany("INSERT INTO opportunitytable (%s) VALUES (%s)" % (",".join(common_columns), ",".join(["%s"] * len(common_columns))), [tuple(item.values()) for item in postgres_data])
    conn.commit()

    # Sync data from Postgres to DynamoDB
    cur.execute("SELECT %s FROM opportunitytable" % ",".join(common_columns))
    postgres_result = cur.fetchall()
    dynamodb_items = []
    for row in postgres_result:
        dynamodb_item = {}
        for i, column in enumerate(common_columns):
            dynamodb_item[column] = {'S': row[i]}
        dynamodb_items.append(dynamodb_item)
    table.batch_write_item(RequestItems=[{'PutRequest': {'Item': item}} for item in dynamodb_items])

def lambda_handler(event, context):
    sync_data()
    print('Data synced successfully!')
    return {'statusCode': 200, 'body': 'Data synced successfully!'}