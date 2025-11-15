import { pool } from '../modules/database/pg.js'

// Change them to dataloaders if needed, but for now each request comes for one team_id only

const gettriggersbyteamid = async (team_id: string) => {
    var query = `SELECT * FROM TriggersInfo WHERE team_id = $1`;
    var values = [team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const gettriggerbytriggerid = async (team_id: string, trigger_id: string) => {
    var query = `SELECT * FROM TriggersInfo WHERE trigger_id = $1 AND team_id = $2`;
    var values = [trigger_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const gettriggerbyteamidandtype = async (team_id: string, platform: string, type: string) => {
    var query = `SELECT * FROM TriggersInfo WHERE platform = $1 AND type = $2 AND team_id = $3`;
    var values = [platform, type, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const gettriggereventsbytriggerid = async (team_id: string, trigger_id: string) => {
    var query = `SELECT event_data, trigger_uuid, timestamp FROM TriggersData WHERE trigger_id = $1 AND team_id = $2 ORDER BY timestamp DESC Limit 10`;
    var values = [trigger_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const gettriggereventbytriggeruuid = async (team_id: string, trigger_uuid: string) => {
    var query = `SELECT event_data FROM TriggersData WHERE trigger_uuid = $1 AND team_id = $2`;
    var values = [trigger_uuid, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

// Insert event data into TriggersData table
const inserttriggerevent = async (team_id: string, trigger_id: string, trigger_uuid: string, event_data: any) => {
    var query = `INSERT INTO TriggersData (team_id, trigger_id, trigger_uuid, event_data) VALUES ($1, $2, $3, $4)`;
    var values = [team_id, trigger_id, trigger_uuid, event_data];
    var res = await pool.query(query, values);
    return res.rows;
}

const getworkflowsbyteamid = async (team_id: string) => {
    var query = `SELECT * FROM workflows WHERE team_id = $1 and is_template = false`;
    var values = [team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const gettemplateworkflowsbyteamid = async (team_id: string) => {
    var query = `SELECT * FROM workflows WHERE team_id = $1 and is_template = true`;
    var values = [team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getworkflowbyworkflowid = async (team_id: string, workflow_id: string) => {
    var query = `SELECT * FROM workflows WHERE workflow_id = $1 AND team_id = $2`;
    var values = [workflow_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const createworkflow = async(team_id: string, workflow_id: string, workflow_name: string, workflow_description: string) => {
    console.log("Creating workflow")
    var query = `INSERT INTO workflows (team_id, workflow_id, workflow_name, workflow_description, trigger_id) VALUES ($1, $2, $3, $4, $5)`;
    var values = [team_id, workflow_id, workflow_name, workflow_description, ''];
    var res = await pool.query(query, values);
    return res.rows;
}

const getworkflowbytemplateid = async (team_id: string, template_id: string) => {
    var query = `SELECT * FROM workflows WHERE template_id = $1 AND team_id = $2`;
    var values = [template_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const createworkflow_from_template = async(team_id: string, workflow_id: string,
    workflow_name: string, workflow_description: string, trigger_id: string,
    template_id: string
    ) => {
    console.log("Creating workflow from template");
    let is_template = true;
    var query = `INSERT INTO workflows (team_id, workflow_id, workflow_name, workflow_description, trigger_id, is_template, template_id) VALUES ($1, $2, $3, $4, $5, $6, $7)`;
    var values = [team_id, workflow_id, workflow_name, workflow_description, trigger_id, is_template, template_id];
    var res = await pool.query(query, values);
    return res.rows;
}
// update workflow_name, workflow_description
const updateworkflowdetails = async(team_id: string, workflow_id: string, workflow_name: string = '', workflow_description: string = '') => {
    var query = `UPDATE workflows SET workflow_name = COALESCE(NULLIF($1, ''), workflow_name),
                    workflow_description = COALESCE(NULLIF($2, ''), workflow_description)
                    WHERE workflow_id = $3 AND team_id = $4`;
    var values = [workflow_name, workflow_description, workflow_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const updateworkflowtemplatestatus = async(team_id: string, template_id: string, status: boolean) => {
    var query = `UPDATE workflows SET status = $1 WHERE template_id = $2 AND team_id = $3`;
    var values = [status, template_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const updateworkflowtrigger = async(team_id: string, workflow_id: string, trigger_id: string) => {
    var query = `UPDATE workflows SET trigger_id = $1 WHERE workflow_id = $2 AND team_id = $3`;
    var values = [trigger_id, workflow_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const updateworkflowstatus = async(team_id: string, workflow_id: string, status: boolean) => {
    var query = `UPDATE workflows SET status = $1 WHERE workflow_id = $2 AND team_id = $3`;
    var values = [status, workflow_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getsessionsbyteamid = async (team_id: string) => {
    var query = `SELECT * FROM workflowdetails WHERE team_id = $1`;
    var values = [team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getsessionsbyworkflowid = async (team_id: string, workflow_id: string) => {
    var query = `SELECT * FROM workflowdetails WHERE workflow_id = $1 AND team_id = $2`;
    var values = [workflow_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getsession = async (team_id: string, workflow_id: string, session_id: string) => {
    var query = `SELECT * FROM workflowdetails WHERE workflow_id = $1 AND session_id = $2 AND team_id = $3`;
    var values = [workflow_id, session_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}


export const triggers_helpers = { gettriggersbyteamid, gettriggereventsbytriggerid, gettriggerbyteamidandtype, gettriggereventbytriggeruuid, gettriggerbytriggerid }

export const workflows_helpers = { getworkflowsbyteamid, getworkflowbyworkflowid, createworkflow, updateworkflowtrigger, updateworkflowstatus, updateworkflowdetails, updateworkflowtemplatestatus, gettemplateworkflowsbyteamid, getworkflowbytemplateid, createworkflow_from_template}

export const sessions_helpers = { getsessionsbyteamid, getsessionsbyworkflowid, getsession }