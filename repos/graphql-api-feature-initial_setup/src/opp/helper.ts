import { pool } from '../modules/database/pg.js'

// Change them to dataloaders if needed, but for now each request comes for one team_id only
    // getformbyopportunity,

const getopportunities = async (team_id: string) => {
    var query = `SELECT * FROM opportunitytable WHERE team = $1`;
    var values = [team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getopportunitybyoppkey = async (opp_key: string) => {
    var query = `SELECT * FROM opportunitytable WHERE opp_key = $1`;
    var values = [opp_key];
    var res = await pool.query(query, values);
    return res.rows;
}

const getopportunitybyteamid = async (team_id: string) => {
    var query = `SELECT * FROM opportunitytable WHERE team = $1`;
    var values = [team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getopportunitybypersonid = async (team_id: string, fub_person_id: string) => {
    var query = `SELECT * FROM opportunitytable WHERE team = $1 AND fub_person_id = $2`;
    var values = [team_id, fub_person_id];
    var res = await pool.query(query, values);
    return res.rows;
}

// Add team id filter
const updateopportunity = async (team_id: string, opp_key: string, fub_person_id: string, opp_type: string, opp_stage: string, lead_last_name: string, custom_opp_data:any) => {
    var query = `UPDATE opportunitytable SET custom_opp_data = $1, opp_type = $2, opp_stage = $3, opp_last_name = $4, fub_person_id = $5 WHERE opp_key = $6`;
    var values = [custom_opp_data, opp_type, opp_stage, lead_last_name, fub_person_id, opp_key];
    var res = await pool.query(query, values);
    return res.rows;
}

const createopportunity = async (team_id: string, opp_key: string, fub_person_id: string, opp_type: string, opp_stage: string, lead_last_name: string, custom_opp_data:any) => {
    var query = `INSERT INTO opportunitytable (team, opp_key, fub_person_id, opp_type, opp_stage, opp_last_name, custom_opp_data)
                VALUES ($1, $2, $3, $4, $5, $6, $7)`;
    var values = [team_id, opp_key, fub_person_id, opp_type, opp_stage, lead_last_name, custom_opp_data];
    var res = await pool.query(query, values);
    return res.rows;
}

const getformsbyteam = async (team_id: string, offset: number, limit: number) => {
    var query = `SELECT * FROM form_data WHERE team_id = $1 AND is_deleted = false ORDER BY form_created_date LIMIT $2 OFFSET $3`;
    var values = [team_id, limit, offset];
    var res = await pool.query(query, values);
    return res.rows;
}

const countformsbyteam = async (team_id: string) => {
    var query = `SELECT COUNT(*) FROM form_data WHERE team_id = $1 AND is_deleted = false`;
    var values = [team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getTeamIdFromFormId = async (form_id: string) => {
    var query = `SELECT team_id FROM form_data WHERE form_id = $1`;
    var values = [form_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getformbyid = async (form_id: string) => {
    var query = `SELECT * FROM form_data WHERE form_id = $1`;
    var values = [form_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getformentrybyid = async (team_id: string, form_entry_id: string) => {
    var query = `SELECT * FROM form_entries WHERE team_id = $1 AND form_entry_id = $2`;
    var values = [team_id, form_entry_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const createform = async (team_id: string, form_id: string, form_name: string, form_description: string, form_fields: any,
    form_conditions: any, status: boolean, form_created_date: string, update_by: string, base_form_template: string,
    logo_url:string, color_scheme:string, form_type:string) => {
//  REVER THIS BEFORE DEPLOYMENT
var query = `INSERT INTO form_data (team_id, form_id, form_name, form_description, form_fields_new, form_conditions, status, form_created_date, update_by, base_form_template, logo_url, color_scheme, form_type)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)`;
var values = [team_id, form_id, form_name, form_description, form_fields, form_conditions, status, form_created_date, update_by, base_form_template, logo_url, color_scheme, form_type];
var res = await pool.query(query, values);
return res.rows;
}

const updateform = async (team_id: string, form_id: string, form_name: string, form_description: string, 
                form_fields: any, form_conditions: any, status: boolean, form_updated_date: string, 
                logo_url: string, color_scheme: string, update_by: string) => {
    var query = `UPDATE form_data SET form_name = $1, form_description = $2, form_fields_new = $3, form_conditions = $4,
                status = $5, form_updated_date = $6, logo_url = $7, color_scheme = $8,
                update_by = $9 WHERE form_id = $10 AND team_id = $11`;
    var values = [form_name, form_description, form_fields, form_conditions, status, form_updated_date, logo_url, color_scheme, update_by, form_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const updateformname = async (team_id: string, form_id: string, form_name: string) => {
    var query = `UPDATE form_data SET form_name = $1 WHERE form_id = $2 AND team_id = $3`;
    var values = [form_name, form_id, team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const deleteform = async (team_id: string, form_id: string) => {
    // var query = `DELETE FROM form_data WHERE team_id = $1 AND form_id = $2`;
    var query = `UPDATE form_data SET is_deleted=true WHERE team_id = $1 AND form_id = $2`;
    var values = [team_id, form_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getentriesbyform = async (team_id: string, form_id: string) => {
    var query = `SELECT * FROM form_entries WHERE team_id = $1 AND form_id = $2 AND is_deleted = false`;
    var values = [team_id, form_id];
    var res = await pool.query(query, values);
    return res.rows;
} 

const createformentry = async (team_id: string, form_id: string, form_entry_id: string, form_entry_data: any) => {
    var query = `INSERT INTO form_entries (team_id, form_id, form_entry_id, form_entry_data)
                VALUES ($1, $2, $3, $4)`;
    var values = [team_id, form_id, form_entry_id, form_entry_data];
    var res = await pool.query(query, values);
    return res.rows;
}

const updateformentry = async (team_id: string, form_id: string, form_entry_id: string, form_entry_data: any) => {
    var query = `UPDATE form_entries SET form_entry_data = $1 WHERE team_id = $2 AND form_id = $3 AND form_entry_id = $4`;
    var values = [form_entry_data, team_id, form_id, form_entry_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const deleteformentry = async (team_id: string, form_id: string, form_entry_id: string) => {
    // var query = `DELETE FROM form_entries WHERE team_id = $1 AND form_id = $2 AND form_entry_id = $3`;
    var query = `UPDATE form_entries SET is_deleted=true WHERE team_id = $1 AND form_id = $2 AND form_entry_id = $3`;
    var values = [team_id, form_id, form_entry_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const bulk_deleteformentry = async (team_id: string, form_id: string) => {
    var query = `DELETE FROM form_entries WHERE team_id = $1 AND form_id = $2`;
    var values = [team_id, form_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const countformentries = async (team_id: string, form_id: string) => {
    var query = `SELECT COUNT(*) FROM form_entries WHERE team_id = $1 AND form_id = $2 AND is_deleted = false`;
    var values = [team_id, form_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const countformentriesbydate = async (team_id: string, form_id: string, date: string) => {
    var query = `SELECT COUNT(*) FROM form_entries WHERE team_id = $1 AND form_id = $2 AND entry_created_date > $3 AND is_deleted = false`;
    var values = [team_id, form_id, date];
    var res = await pool.query(query, values);
    return res.rows;
}

const createcustomfield = async (team_id: string, field_id: string, field_name: string,  field_description: string, field_type: string, 
    settings: any, linked_to:string) => {
    var query = `INSERT INTO form_custom_fields (team_id, field_id, field_name, field_type, field_description, settings, linked_to)
                VALUES ($1, $2, $3, $4, $5, $6, $7)`;
    var values = [team_id, field_id, field_name, field_type, field_description, settings, linked_to];
    var res = await pool.query(query, values);
    return res.rows;
}

const getcustomfields = async (team_id: string) => {
    var query = `SELECT * FROM form_custom_fields WHERE team_id = $1`;
    var values = [team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getfieldbyid = async (team_id: string, field_id: string) => {
    var query = `SELECT field_id, field_name, field_type, input_type, field_settings as settings FROM field_data WHERE team_id = $1 AND field_id = $2`;
    var values = [team_id, field_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getfieldsbyteamid = async (team_id: string) => {
    var query = `SELECT field_id, field_name, field_type, input_type, field_settings as settings FROM field_data WHERE team_id = $1`;
    var values = [team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getformfields = async (team_id: string, form_id: string) => {
    var query = `SELECT field_id as elementid, input_type as type, field_name as name, field_settings as settings FROM field_data WHERE team_id = $1 and field_id = Any(Array(SELECT form_fields_new FROM form_data WHERE form_id = $2));`;
    var values = [team_id, form_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const getfieldnames = async (team_id: string, form_id: string) => {
    var query = `SELECT field_id, field_name FROM field_data WHERE team_id = $1 and field_id = Any(Array(SELECT form_fields_new FROM form_data WHERE form_id = $2));`;
    var values = [team_id, form_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const createfield = async (team_id: string, field_id: string, field_name: string, input_type: string, field_type: string, field_settings: JSON, field_id_team_id: string) => {
    var query = `INSERT INTO field_data (team_id, field_id, field_name, input_type, field_type, field_settings, field_id_team_id)
                VALUES ($1, $2, $3, $4, $5, $6, $7)`;
    var values = [team_id, field_id, field_name, input_type, field_type, field_settings, field_id_team_id];
    var res = await pool.query(query, values);
    return res.rows;
}

const updatefieldbyid = async (field_name: string, input_type:string, field_settings: JSON, field_id_team_id: string) => {
    var query = `UPDATE field_data SET field_name = $1, input_type = $2, field_settings = $3 WHERE field_id_team_id = $4`;
    var values = [field_name, input_type, field_settings, field_id_team_id];
    var res = await pool.query(query, values);
    return res.rows;
}



export const form_helpers = { createform, updateform, updateformname, getformbyid, getformsbyteam, deleteform, getTeamIdFromFormId, countformsbyteam}

export const form_entries = { getentriesbyform, createformentry, updateformentry, deleteformentry, countformentries, countformentriesbydate, getformentrybyid }

export const opportunity = { getopportunities, getopportunitybyoppkey, getopportunitybyteamid, getopportunitybypersonid, updateopportunity, createopportunity }

export const fields = { createcustomfield, getcustomfields, getfieldbyid, getfieldsbyteamid, getformfields, createfield, updatefieldbyid, getfieldnames }
