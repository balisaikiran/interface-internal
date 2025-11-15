import {form_helpers, form_entries, opportunity, fields } from "./helper.js"
import fetch, { Response } from "node-fetch";
import { randomUUID } from "crypto";
import { pool } from '../modules/database/pg.js'
import { count } from "console";


export const resolvers = {
    Query: {
        Opps: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var opportunities = await opportunity.getopportunities(team_id);
            console.log("opportunities", opportunities)
            return opportunities
        },

        opportunity: async (parent, args, context, info) => {
            // var team_id: string = args.team_id;
            var opp_key: string = args.opp_key;
            // var person_id: string = args.person_id;
            // if else conition to check if opp_key is present or not
            var opportunity_data = await opportunity.getopportunitybyoppkey(opp_key);
            console.log("opportunity_data", opportunity_data)
            return opportunity_data[0]
        },

        opportunitiesByPersonId: async (parent, args, context, info) => {
            var team_id: string = args.team_id;
            var fub_person_id: string = args.fub_person_id;
            var opportunity_data = await opportunity.getopportunitybypersonid(team_id, fub_person_id);
            return opportunity_data
        },

        formEntries: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var form_entries_data = await form_entries.getentriesbyform(team_id, form_id);
            return form_entries_data
        },

        formEntry: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            // var form_id: string = args.form_id;
            var form_entry_id: string = args.form_entry_id;
            var form_entry_data = await form_entries.getformentrybyid(team_id, form_entry_id);
            if (form_entry_data.length == 0) {
                return form_entry_data
            }
            console.log("FORM ENTRY:", form_entry_data)
            return form_entry_data[0]
        },

        countFormEntries: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var count = await form_entries.countformentries(team_id, form_id);
            console.log("COUNT:", count)
            return count[0]
        },

        countFormEntriesToday: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var date: string = new Date(new Date().setDate(new Date().getDate()-1)).toISOString().slice(0, 10)
            console.log("DATE:", date)
            var count = await form_entries.countformentriesbydate(team_id, form_id, date);
            return count[0]
        },

        countTotalForms: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var count = await form_helpers.countformsbyteam(team_id);
            return count[0]
        },

        forms: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            let offset: number = args.offset || 0;
            let limit: number = 10;
            var forms = await form_helpers.getformsbyteam(team_id, offset, limit);
            return forms
        },

        formsNames: async (parent, args, context, info) => {
            let team_id: string = args.team_id;
            let offset: number = 0;
            let limit: number = 100;
            var forms = await form_helpers.getformsbyteam(team_id, offset, limit);
            return forms
        },

        formData: async (parent, args, context, info) => {
            // removed team_id from args for publicly accessible forms
            // var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var form = await form_helpers.getformbyid(form_id);
            if (form.length == 0) {
                return form
            }
            var resp = form[0];
            console.log("FORM:", form)
            var team_id = resp.team_id;
            let form_fields = resp.form_fields || [];
            let form_fields_length = form_fields.length;
            if (form_fields_length == 0) {
                resp["form_fields"] = [];
                return resp
            }
            else {
                let form_fields_data = await fields.getformfields(team_id, form_id);
                // let form_fields_ordered_list = form_fields.map((field: any) => {
                //     console.log("FIELD MAPPING:", field.field_id, form_fields_unordered_list.find((a: any) => a.field_id === field.field_id))
                //     return form_fields_unordered_list.find((a: any) => a.field_id === field.field_id)
                // })
                form_fields_data.sort((a, b) => form_fields.indexOf(a.field_id) - form_fields.indexOf(b.field_id));
                console.log("FORM FIELDS:", form_fields, form_fields.length)
                resp["form_fields"] = form_fields_data;
            }
            console.log("RESP:", resp)
            return resp
        },

        GetCustomFields: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var custom_fields = await fields.getcustomfields(team_id);
            return custom_fields
        },

        GetFormFields: async (parent, args, context, info) => {
            // var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var team_id: string = args.team_id;
            var form_fields = await fields.getformfields(team_id, form_id);
            return form_fields
        },

        GetFieldById: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var field_id: string = args.field_id;
            var field = await fields.getfieldbyid(team_id, field_id);
            if (field.length == 0) {
                return field
            }
            return field[0]
        },

        GetFieldsByTeamId: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var fields_resp = await fields.getfieldsbyteamid(team_id);
            return fields_resp
        }

    },

    Mutation: {
        CreateForm: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = randomUUID();
            var form_name: string = args.form_data.form_name;
            var form_description: string = args.form_data.form_description;
            var form_fields: any = args.form_data.form_fields;
            var form_conditions: any = args.form_data.form_conditions;
            var status: boolean = args.form_data.status;
            var form_created_date: string = new Date().toISOString();
            var update_by: string = "admin";
            var base_form_template: string = args.form_data.base_form_template;
            var logo_url: string = args.form_data.logo_url;
            var color_scheme: string = args.form_data.color_scheme;
            var form_type: string = args.form_data.form_type;
            var form = await form_helpers.createform(team_id, form_id, form_name, form_description, form_fields, form_conditions, status, form_created_date, update_by, base_form_template, logo_url, color_scheme, form_type);
            console.log("FORM:", form)
            return {"team_id": team_id, "form_id": form_id}
        },

        UpdateForm: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var form_name: string = args.form_data.form_name;
            var form_description: string = args.form_data.form_description;
            var form_fields: any = args.form_data.form_fields;
            var form_conditions: any = args.form_data.form_conditions;
            var status: boolean = args.form_data.status;
            var form_updated_date: string = new Date().toISOString();
            var logo_url: string = args.form_data.logo_url;
            var color_scheme: string = args.form_data.color_scheme;
            var update_by: string = "admin";
            console.log("FORM Description DATA:", args.form_data.form_description)
            var form = await form_helpers.updateform(team_id, form_id, form_name, form_description, form_fields, form_conditions, status, form_updated_date, logo_url, color_scheme, update_by);
            console.log("FORM:", form)
            return {"team_id": team_id, "form_id": form_id}
        },

        UpdateFormName: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var form_name: string = args.form_name;
            console.log("FORM Description DATA:", team_id, form_id, form_name);
            var form = await form_helpers.updateformname(team_id, form_id, form_name);
            console.log("FORM:", form)
            return {"team_id": team_id, "form_id": form_id}
        },
            
        DeleteForm: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var form = await form_helpers.deleteform(team_id, form_id);
            console.log("FORM:", form)
            return {"team_id": team_id, "form_id": form_id}
        },

        DuplicateForm: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var form_data = await form_helpers.getformbyid(form_id);
            console.log("FORM DATA:", form_data)
            var form_id: string = randomUUID();
            var form_name: string = form_data[0].form_name + " (Copy)";
            var form_description: string = form_data[0].form_description;
            var form_fields: any = form_data[0].form_fields;
            var form_conditions: any = form_data[0].form_conditions;
            var status: boolean = form_data[0].status;
            var form_created_date: string = new Date().toISOString();
            var update_by: string = "admin";
            var base_form_template: string = form_data[0].base_form_template;
            var logo_url: string = args.form_data.logo_url;
            var color_scheme: string = args.form_data.color_scheme;
            var form_type: string = args.form_data.form_type;
            var form = await form_helpers.createform(team_id, form_id, form_name, form_description, form_fields, form_conditions, status, form_created_date, update_by, base_form_template, logo_url, color_scheme, form_type);
            console.log("FORM:", form)
            return {"team_id": team_id, "form_id": form_id, "form_name": form_name, "form_description": form_description, "form_fields": form_fields, 
                    "form_conditions": form_conditions, "status": status, "form_created_date": form_created_date, "update_by": update_by, "base_form_template": base_form_template}
        },

        CreateFormEntry: async (parent, args, context, info) => {
            console.log("INSIDE CREATE FORM ENTRY")
            var form_id: string = args.form_id;
            console.log("FORM ID:", form_id)
            let response = await form_helpers.getTeamIdFromFormId(form_id);
            let team_id = response[0]['team_id'];
            console.log("TEAM ID:", team_id)
            var form_entry_id: string = randomUUID();
            var form_entry_data: any = args.form_entry_data;
            console.log("FORM ENTRY DATA:", team_id, form_id, form_entry_id, form_entry_data)
            var form_entry = await form_entries.createformentry(team_id, form_id, form_entry_id, form_entry_data);
            console.log("FORM ENTRY:", form_entry)
            return {"form_id": form_id, "form_entry_id": form_entry_id}
        },

        UpdateFormEntry: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var form_entry_id: string = args.form_entry_id;
            var form_entry_data: any = args.form_entry_data;
            var form_entry = await form_entries.updateformentry(team_id, form_id, form_entry_id, form_entry_data);
            console.log("FORM ENTRY:", form_entry)
            return {"form_id": form_id, "form_entry_id": form_entry_id}
        },

        DeleteFormEntry: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var form_id: string = args.form_id;
            var form_entry_id: string = args.form_entry_id;
            var form_entry = await form_entries.deleteformentry(team_id, form_id, form_entry_id);
            console.log("FORM ENTRY:", form_entry)
            console.log("FORM ENTRY:", {"form_id": form_id, "form_entry_id": form_entry_id})
            return {"form_id": form_id, "form_entry_id": form_entry_id}
        },

        CreateCustomField: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var custom_fields: any = args.custom_fields;
            var field_id: string = args.custom_fields.field_id;
            var field_name: string = args.custom_fields.field_name;
            var field_description: string = args.custom_fields.field_description;
            var field_type: string = args.custom_fields.field_type;
            var settings: any = args.custom_fields.settings;
            console.log("SETTINGS:", settings);
            var linked_to: string = args.custom_fields.linked_to;
            var custom_field = await fields.createcustomfield(team_id, field_id, field_name, field_description, field_type, settings, linked_to);
            console.log("CUSTOM FIELD:", custom_field)
            return {"field_id": field_id, "field_type": field_type, "field_name": field_name}
        },

        CreateOpp: async (parent, args, context, info) => {
            let form_id: string = args.form_id;
            let resp = await form_helpers.getTeamIdFromFormId(form_id);
            let team_id = resp[0]['team_id'];
            var opp_key: string = team_id+'-'+randomUUID();
            console.log("OPP KEY:", opp_key)
            var opp_data: any = args.opp_data;
            let fub_person_id = opp_data['InputField-Follow-up-boss-lead-id'];
            let opp_type = opp_data['InputField-opp_type'];
            let opp_stage = opp_data['InputField-opp_stage'];
            let lead_last_name = opp_data['InputField-opp_last_name'];
            let field_data = await fields.getfieldnames(team_id, form_id);
            console.log("FIELD DATA:", field_data);
            let note_payload = {}
            for (let key in opp_data) {
                let field_def = field_data.find((field: any) => field.field_id === key);
                if (field_def) {
                    let field_name = field_def.field_name || key; 
                    note_payload[field_name] = opp_data[key]
                }
                else {
                    note_payload[key] = opp_data[key]
                }
            }
            console.log("NOTE PAYLOAD:", note_payload)
            let custom_opp_data = {}

            let url = "https://wiqog2w5m8.execute-api.us-west-2.amazonaws.com/createFubNote"; // Dev
            // let url = " https://3vrfd0zlta.execute-api.us-west-2.amazonaws.com/createFubNote"; // Prod
            let payload = {"team_id": team_id, "opp_key": opp_key, "fub_person_id": fub_person_id, "note_payload": note_payload}
            const response = fetch(url, {
                method: "POST",
                body: JSON.stringify(payload),
            });
            var opp = await opportunity.createopportunity(team_id, opp_key, fub_person_id, opp_type, opp_stage, lead_last_name, custom_opp_data);
            console.log("OPP:", opp)
            return {"opp_key": opp_key}
        },

        UpdateOpp: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            // var opp_key: string = args.opp_key;
            let opp_data: any = args.opp_data;
            let form_id = args.form_id;
            let fub_person_id = opp_data['InputField-Follow-up-boss-lead-id'];
            let opp_type = opp_data['InputField-opp_type'];
            let opp_stage = opp_data['InputField-opp_stage'];
            let lead_last_name = opp_data['InputField-opp_last_name'];
            let opp_key = opp_data['InputField-opp_key'];
            let custom_opp_data = {}
            console.log("OPP DATA:", opp_data, form_id, opp_key);
            let field_data = await fields.getfieldnames(team_id, form_id);
            let note_payload = {}
            for (let key in opp_data) {
                let field_def = field_data.find((field: any) => field.field_id === key);
                if (field_def) {
                    let field_name = field_def.field_name || key; 
                    note_payload[field_name] = opp_data[key]
                }
                else {
                    note_payload[key] = opp_data[key]
                }
            }
            console.log("NOTE PAYLOAD:", note_payload)

            let url = "https://wiqog2w5m8.execute-api.us-west-2.amazonaws.com/createFubNote"; // Dev
            // let url = " https://3vrfd0zlta.execute-api.us-west-2.amazonaws.com/createFubNote"; // Prod
            let payload = {"team_id": team_id, "opp_key": opp_key, "fub_person_id": fub_person_id, "note_payload": note_payload}
            const response = fetch(url, {
                method: "POST",
                body: JSON.stringify(payload),
            });
            var opp = await opportunity.updateopportunity(team_id, opp_key, fub_person_id, opp_type, opp_stage, lead_last_name, custom_opp_data);
            return {"opp_key": opp_key}
        },

        CreateField: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var field_data: any = args.field_data;
            var field_id: string = field_data.field_id;
            var field_name: string = field_data.field_name;
            var input_type: string = field_data.input_type;
            var field_type: string = field_data.field_type;
            var settings: any = field_data.settings;
            var field_id_team_id: string = field_id+'-'+team_id
            var field = await fields.createfield(team_id, field_id, field_name, input_type, field_type, settings, field_id_team_id);
            console.log("FIELD:", field)
            return {"team_id": team_id, "field_id": field_id}
        },

        UpdateField: async (parent, args, context, info) => {
            console.log("INSIDE UPDATE FIELD")
            var team_id: string = context.team_id;
            var field_id: string = args.field_id;
            var field_data: any = args.field_data;
            console.log("FIELD DATA:", field_data)
            var field_name: string = field_data.settings.placeHolder;
            var input_type: string = field_data.input_type;
            var settings: any = field_data.settings;
            let field_id_team_id: string = field_id+'-'+team_id;
            console.log("FIELD ID TEAM ID:", field_id_team_id, field_name, input_type, settings, field_id_team_id);
            var field = await fields.updatefieldbyid(field_name, input_type, settings, field_id_team_id);
            console.log("FIELD:", field)
            return {"team_id": team_id, "field_id": field_id}
        },
    }
}
