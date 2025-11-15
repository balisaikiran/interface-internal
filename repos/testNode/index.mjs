import pg from 'pg';
const { Client } = pg;

export const handler = async (event) => {
  const dbConfig = {
    host: "dev-database-2.cmbltiirvdvj.us-west-2.rds.amazonaws.com",
    database: "postgres",
    user: "postgres_user",
    password: "Dev#test#23",
    port: 5432
  };

  const client = new Client(dbConfig);
  try {
    await client.connect();
  } catch (err) {
    console.error('Error connecting to PostgreSQL:', err);
    throw err;
  }

  try {
    if (!Array.isArray(event.Records)) {
      console.error('Error processing DynamoDB stream event: event.Records is not an array');
      return {
        statusCode: 400,
        body: JSON.stringify('Error processing DynamoDB stream event: event.Records is not an array')
      };
    }

    for (const record of event.Records) {
      if (record.eventName === 'MODIFY') {
        const newImage = record.dynamodb.NewImage;
        
        console.log('NewImage:', JSON.stringify(newImage, null, 2)); // Log the NewImage object

        // Ensure all required properties exist
        const id = newImage.id?.S;
        if (!id) {
          console.error('Missing required property: id');
          continue;
        }

        const isu_client_updated_ts = newImage.isu_client_updated_ts?.S;
        const opp_updated_ts = newImage.opp_updated_ts?.S;
        const opp_stage = newImage.opp_stage?.S;
        const fub_deal_created_ts = newImage.fub_deal_created_ts?.S;
        const opp_type = newImage.opp_type?.S;
        const opp_appt_date = newImage.opp_appt_date?.S;
        const fub_deal_stage_name = newImage.fub_deal_stage_name?.S;
        const opp_appt_met_date = newImage.opp_appt_met_date?.S;
        const fub_person_id = newImage.fub_person_id?.S;
        const opp_price = newImage.opp_price?.N;
        const isu_client_created_ts = newImage.isu_client_created_ts?.S;
        const opp_created_ts = newImage.opp_created_ts?.S;
        const fub_deal_id = newImage.fub_deal_id?.S;
        const opp_appt_disposition = newImage.opp_appt_disposition?.S;
        const teamfubdealid = newImage.teamfubdealid?.S;
        const team = newImage.team?.S;
        const fub_deal_entered_stage_ts = newImage.fub_deal_entered_stage_ts?.S;
        const isu_client_id = newImage.isu_client_id?.S;
        const opp_assigned_osa = newImage.opp_assigned_osa?.S;
        const opp_isa = newImage.opp_isa?.S;
        const opp_notes = newImage.opp_notes?.S;
        const opp_address = newImage.opp_address?.S;
        const opp_agreement_expiration_date = newImage.opp_agreement_expiration_date?.S;
        const appt_set_entry_id = newImage.appt_set_entry_id?.S;
        const fub_appt_start_time = newImage.fub_appt_start_time?.S;
        const opp_commission_percent = newImage.opp_commission_percent?.N;
        const fub_original_appt_start_time = newImage.fub_original_appt_start_time?.S;
        const disp_text_wait_timestamp = newImage.disp_text_wait_timestamp?.S;
        const appt_set_lead_type = newImage.appt_set_lead_type?.S;
        const appt_set_platform = newImage.appt_set_platform?.S;
        const disp_text_original_wait_timestamp = newImage.disp_text_original_wait_timestamp?.S;
        const opp_address2 = newImage.opp_address2?.S;
        const opp_city = newImage.opp_city?.S;
        const opp_postal_code = newImage.opp_postal_code?.S;
        const opp_last_name = newImage.opp_last_name?.S;
        const opp_state = newImage.opp_state?.S;
        const previous_opp_stage = newImage.previous_opp_stage?.S;
        const createentryid = newImage.createentryid?.S;
        const createformid = newImage.createformid?.S;

        const query = `
          UPDATE opportunitytable
          SET
            isu_client_updated_ts = $1,
            opp_updated_ts = $2,
            opp_stage = $3,
            fub_deal_created_ts = $4,
            opp_type = $5,
            opp_appt_date = $6,
            fub_deal_stage_name = $7,
            opp_appt_met_date = $8,
            fub_person_id = $9,
            opp_price = $10,
            isu_client_created_ts = $11,
            opp_created_ts = $12,
            fub_deal_id = $13,
            opp_appt_disposition = $14,
            teamfubdealid = $15,
            team = $16,
            fub_deal_entered_stage_ts = $17,
            isu_client_id = $18,
            opp_assigned_osa = $19,
            opp_isa = $20,
            opp_notes = $21,
            opp_address = $22,
            opp_agreement_expiration_date = $23,
            appt_set_entry_id = $24,
            fub_appt_start_time = $25,
            opp_commission_percent = $26,
            fub_original_appt_start_time = $27,
            disp_text_wait_timestamp = $28,
            appt_set_lead_type = $29,
            appt_set_platform = $30,
            disp_text_original_wait_timestamp = $31,
            opp_address2 = $32,
            opp_city = $33,
            opp_postal_code = $34,
            opp_last_name = $35,
            opp_state = $36,
            previous_opp_stage = $37,
            createentryid = $38,
            createformid = $39
          WHERE id = $40
        `;

        const values = [
          isu_client_updated_ts, opp_updated_ts, opp_stage, fub_deal_created_ts, opp_type, opp_appt_date,
          fub_deal_stage_name, opp_appt_met_date, fub_person_id, opp_price, isu_client_created_ts, opp_created_ts,
          fub_deal_id, opp_appt_disposition, teamfubdealid, team, fub_deal_entered_stage_ts, isu_client_id,
          opp_assigned_osa, opp_isa, opp_notes, opp_address, opp_agreement_expiration_date, appt_set_entry_id,
          fub_appt_start_time, opp_commission_percent, fub_original_appt_start_time, disp_text_wait_timestamp,
          appt_set_lead_type, appt_set_platform, disp_text_original_wait_timestamp, opp_address2, opp_city,
          opp_postal_code, opp_last_name, opp_state, previous_opp_stage, createentryid, createformid, id
        ];

        await client.query(query, values);
      }
    }
  } catch (error) {
    console.error('Error processing DynamoDB stream event:', error);
    throw error;
  } finally {
    await client.end();
  }

  return {
    statusCode: 200,
    body: JSON.stringify('Processed successfully')
  };
};