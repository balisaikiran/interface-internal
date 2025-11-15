import {
    getactionsbyworkflowid,
    updateworkflow_action,
    deleteworkflow_action,
    getWorkflowSession
} from "./helper_dynamodb.js"
import { triggers_helpers, workflows_helpers, sessions_helpers } from "./helper.js"
import { randomUUID } from "crypto";
import { triggers as fubtriggers } from "../fub/triggers.js"
import { pool } from '../modules/database/pg.js'
import { templates, template_workflows } from "./templates.js"
import {creaateFubTrigger} from "../fub/trigger_helper.js"
import{setup_fub_for_template} from "../fub/template_helpers.js"

// const userLoader = new DataLoader(keys => myBatchGetUsers(keys));
const updateworkflowtrigger = async  (team_id, trigger_id, workflow_id) =>{
    var trigger_details = await triggers_helpers.gettriggerbytriggerid(team_id, trigger_id);
    if (trigger_details.length == 0) {
        // throw new Error("Trigger not found");
        return { "statusCode": 400, "message": "Trigger not found" };
    }
    var trigger_details = trigger_details[0];
    var platform = trigger_details["platform"];
    var type = trigger_details["type"];

    const client = await pool.connect();
    var query = `UPDATE workflows SET trigger_id = $1 WHERE workflow_id = $2 AND team_id = $3`;
    var values = [trigger_id, workflow_id, team_id];
    await client.query("BEGIN");
    let updateresp = await client.query(query, values)
    if (updateresp["rowCount"] == 0) {
        client.query("ROLLBACK");
        client.release();
        // throw new Error("Couldnot find Workflow");
        return { "statusCode": 400, "message": "Couldnot find Workflow" };

    }
    // var response = await updateworkflow_action(workflow_id=workflow_id, "trigger", context.dynamodbdatabaseloaders, { data_mapper: trigger_data});
    var response = { "$metadata": { "httpStatusCode": 200 } }
    // console.log("response", response)
    if (response["$metadata"]["httpStatusCode"] > 300) {
        // console.log("Error in updating workflow action")
        client.query("ROLLBACK");
        client.release();
        // throw new Error("Error updating workflow trigger");
        // We can also throw an error, and graphql will catch it and return it to the client
        return { "statusCode": 500, "message": "Error updating workflow trigger" };
    }
    await client.query("COMMIT");
    await client.release();
    return { "statusCode": 200, "message": "" };
}

const update_actions = async (workflow_id, actions_info, dynamodbdatabaseloaders) => {

    if (actions_info.constructor.name == "Object") {
        // Not used, Had written for future use
        for (let [action_id, action_info] of Object.entries(actions_info)) {
            var response = await updateworkflow_action(workflow_id, action_id, dynamodbdatabaseloaders, action_info);
            if (response["$metadata"]["httpStatusCode"] != 200) {
                return { "statusCode": 500, "message": "Internal Server Error" };
            }
            let database_action_ids = (await getactionsbyworkflowid(workflow_id, dynamodbdatabaseloaders)).map((action) => action.action_id);
            let input_action_ids = Object.keys(actions_info);
            // remove extra actions from database
            let extra_action_ids = database_action_ids.filter((action_id) => !input_action_ids.includes(action_id)).map((action_id) => action_id);
            for (var i = 0; i < extra_action_ids.length; i++) {
                let action_id = extra_action_ids[i];
                // delete action
                let resp = await deleteworkflow_action(workflow_id, action_id, dynamodbdatabaseloaders);
                // if (response["$metadata"]["httpStatusCode"] != 200) {
                //     return { "statusCode": 500, "message": "Internal Server Error" };
                // }
            }
        }
    }
    else if (actions_info.constructor.name == "Array") {
        var database_action_ids = (await getactionsbyworkflowid(workflow_id, dynamodbdatabaseloaders)).map((action) => action.action_id);
        var input_action_ids = actions_info.map((action) => action.action_id);

        for (var i = 0; i < actions_info.length; i++) {
            var action_info = actions_info[i];
            // console.log("action_info", action_info)
            var response = await updateworkflow_action(workflow_id, action_info["action_id"], dynamodbdatabaseloaders, action_info);
            // console.log("response updateaction", response)
            if (response["$metadata"]["httpStatusCode"] != 200) {
                return { "statusCode": 500, "message": "Internal Server Error" };
            }
        }

        // remove extra actions from database
        var extra_action_ids = []
        if (input_action_ids.length >= 1) {
            // console.log("input_action_ids", input_action_ids)
            extra_action_ids = database_action_ids.filter((action_id) => !input_action_ids.includes(action_id)).map((action_id) => action_id);
        }
        else {
            extra_action_ids = [];
        }
        // console.log("extra_action_ids", extra_action_ids)
        for (var i = 0; i < extra_action_ids.length; i++) {
            var action_id = extra_action_ids[i];
            // delete action
            var resp = await deleteworkflow_action(workflow_id, action_id, dynamodbdatabaseloaders);
            // if (response["$metadata"]["httpStatusCode"] != 200) {
            //     return { "statusCode": 500, "message": "Internal Server Error" };
            // }
        }
    }
    else {
        // throw new Error("actions_info should be an object");
        return { "statusCode": 500, "message": "Internal Server Error" };

    }
    return { "statusCode": 200, "message": "" };

}
export const resolvers = {
    Query: {
        TriggerEvents: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var trigger_id: string = args.trigger_id;
            // var triggers = await gettriggereventsbytriggerid(trigger_id, context.dynamodbdatabaseloaders);
            var triggers = await triggers_helpers.gettriggereventsbytriggerid(team_id, trigger_id);
            // console.log("Trigger", triggers)
            // Return first trigger, we don't want multiple triggers with same trigger_id, but there can be in the table, fix this later
            return triggers
        },
        TriggerEvent: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            // var trigger_id: string = args.trigger_id;
            var trigger_uuid: string = args.trigger_uuid;
            var triggers = await triggers_helpers.gettriggereventbytriggeruuid(team_id, trigger_uuid);
            // console.log("Trigger", triggers)
            // Return first trigger, we don't want multiple triggers with same trigger_id, but there can be in the table, fix this later
            return triggers[0];
        },
        TestTrigger: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var trigger_id: string = args.trigger_id;
            // var triggers = await gettriggereventsbytriggerid(trigger_id, context.dynamodbdatabaseloaders);
            var triggers = await triggers_helpers.gettriggereventsbytriggerid(team_id, trigger_id);
            let session_id = 'TestSessoin'
            if (triggers.length == 0) {
                return { event_data: {}, trigger_id: trigger_id, session_id: session_id, trigger_uuid: "" }
            }
            // console.log("Trigger", triggers)
            return {
                event_data: triggers[0].event_data,
                trigger_uuid: triggers[0].trigger_uuid,
                session_id: session_id, trigger_id: trigger_id
            }
        },
        Workflows: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var workflows = await workflows_helpers.getworkflowsbyteamid(team_id);
            // var triggers = await gettriggersbyteamid(team_id, context.dynamodbdatabaseloaders);
            // console.log("getworkflowsbyteamid workflows", workflows)
            return workflows
        },
        Workflow: async (parent, args, context, info) => {

            var team_id: string = context.team_id;
            var workflow_id: string = args.workflow_id;
            var workflow = await workflows_helpers.getworkflowbyworkflowid(team_id, workflow_id);
            // Return first trigger, we don't want multiple triggers with same trigger_id, but there can be in the table, fix this later
            return workflow[0];
        },
        WorkflowSessions: async (parent, args, context, info) => {
            let workflow_id: string = args.workflow_id;
            let team_id = context.team_id
            // Use this function to get all sessions for a workflow
            // var workflowsSessions = await getTestActionSessionsByWorkflow(`${team_id}-${workflow_id}-test_action`, context.dynamodbdatabaseloaders)
            // return workflowsSessions
        },
        TestSession: async (parent, args, context, info) => {
            let workflow_id: string = args.workflow_id;
            let team_id = context.team_id
            let session_id = `${team_id}-${workflow_id}-test_action`
            var SessionInfo = await getWorkflowSession(session_id, context.dynamodbdatabaseloaders)
            // convert list of actions to dict
            var workflowsSessions = {}
            for (var i = 0; i < SessionInfo.length; i++) {
                var action = SessionInfo[i];
                workflowsSessions[action.action_id] = action;
            }
            return { "statusCode": 200, "message": "" , "data": workflowsSessions};
        },
        GetAvailableTriggers: async (_: any, args: any, context: any) => {
            // Use this team id to filter out the triggers
            // var team_id = context.team_id;
            // fetch all triggers from database for this team_id
            // var usertriggers = await triggers_helpers.gettriggersbyteamid(team_id);
            var triggers = {
                "FUB": fubtriggers,
            }
            // attach trigger_id to each trigger based on platform, type
            // for (var i = 0; i < usertriggers.length; i++) {
            //     console.log("Trigger", usertriggers[i])
            //     let trigger = usertriggers[i];
            //     if (!(trigger["platform"] in triggers)) {
            //         triggers[trigger["platform"]] = {};
            //     }
            //     if (!(trigger["type"] in triggers[trigger["platform"]])) {
            //         console.log("Trigger not found in triggers", trigger["platform"], trigger["type"])
            //         continue
            //         // triggers[trigger["platform"]][trigger["type"]] = {name: trigger["name"], description: trigger["description"]};
            //     }
            //     // We can make it a list of trigger_ids, but for now we will just keep one
            //     // triggers[trigger["platform"]][trigger["type"]]["trigger_id"] = trigger["trigger_id"];
            // }
            return { "data": triggers, "statusCode": 200 };
        },
        GetTemplates: async (_: any, args: any, context: any) => {
            let team_id = context.team_id;
            let template_workflows = await workflows_helpers.gettemplateworkflowsbyteamid(team_id);
            console.log("template_workflows", template_workflows)
            // deep copy templates
            let usertemplates = JSON.parse(JSON.stringify(templates));
            // get status from template_workflows and add it to templates, iterate over templates
            for (var i = 0; i < templates.length; i++) {
                let template = usertemplates[i];
                let template_id = template['template_id'];
                let template_workflow = template_workflows.filter((template_workflow) => template_workflow['template_id'] == template_id);
                console.log("template_workflow", template_workflow)
                if (template_workflow.length == 1) {
                    console.log("Matched template_workflow", template_workflow)
                    template['status'] = template_workflow[0]['status'];
                }
            }
            return usertemplates;
        }
    },
    Mutation: {
        CreateWorkflow: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var workflow_name = args.workflow_name;
            var workflow_description = args.workflow_description;
            var workflow_id = randomUUID().replace(/-/g, '');
            await workflows_helpers.createworkflow(team_id, workflow_id, workflow_name, workflow_description);
            // Return first trigger, we don't want multiple triggers with same trigger_id, but there can be in the table, fix this later
            return { "workflow_id": workflow_id, "team_id": team_id };
        },
        UpdateWorkflowDetails: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var workflow_id: string = args.workflow_id;
            var workflow_name: string = args.workflow_name;
            var workflow_description: string = args.workflow_description;
            var workflows = await workflows_helpers.getworkflowbyworkflowid(team_id, workflow_id);
            if (workflows.length == 0) {
                return { "statusCode": 500, "message": "Workflow not found" };
            }
            var workflows = await workflows_helpers.updateworkflowdetails(team_id, workflow_id, workflow_name, workflow_description);
            // Return first trigger, we don't want multiple triggers with same trigger_id, but there can be in the table, fix this later
            return { "statusCode": 200, "message": "" };
        },
        UpdateWorkflowTrigger: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var trigger_data = args.trigger_data;
            var workflow_id = args.workflow_id;
            var trigger_id = trigger_data.data_mapper?.trigger_id;
            // console.log("Ending UpdateWorkflowTrigger")
            // var trigger = workflows_helpers.updateworkflowtrigger(team_id, workflow_id, trigger_id);
            // Return first trigger, we don't want multiple triggers with same trigger_id, but there can be in the table, fix this later
            return await updateworkflowtrigger(team_id, trigger_id, workflow_id);
        },
        UpdateWorkflowActions: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var workflow_id: string = args.workflow_id;
            var actions_info: any = args.actions_info;

            var workflows = await workflows_helpers.getworkflowbyworkflowid(team_id, workflow_id);
            if (workflows.length == 0) {
                throw new Error("Workflow not found");
            }
            return update_actions(workflow_id, actions_info, context.dynamodbdatabaseloaders);
        },
        UpdateSession: async (parent, args, context, info) => {
            var session_id = args.session_id;
            var team_id: string = context.team_id;
            var workflow_id: string = args.workflow_id;
            var action_id: string = args.action_id;
            var trigger_uuid: string = args.trigger_uuid;
            // get triggerevent
            var triggerevent = await triggers_helpers.gettriggereventbytriggeruuid(team_id, trigger_uuid);
        },
        UpdateWorkflowStatus: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var workflow_id: string = args.workflow_id;
            var status: boolean = args.status;
            var workflows = await workflows_helpers.updateworkflowstatus(team_id, workflow_id, status);
            // Return first trigger, we don't want multiple triggers with same trigger_id, but there can be in the table, fix this later
            return { "statusCode": 200, "message": "" };
        },
        UpdateWorkflowTemplateStatus: async (parent, args, context, info) => {
            var team_id: string = context.team_id;
            var template_id: string = args.template_id;
            var status: boolean = args.status;
            let _keys = await context.keys.load(team_id);
            let keys = JSON.parse(_keys);
            console.log("keys", keys)
            console.log(keys["fub_key"], Object.keys(keys))
            console.log("-------")
            let _info = templates.filter((template) => template.template_id == template_id);
            if  (_info.length == 0) {
                return { "statusCode": 500, "message": "Template Not found" };
            }
            let template_info = JSON.parse(JSON.stringify(_info));
            console.log("UpdateWorkflowTemplateStatus", team_id, template_id, status)
            // get template by id
            var user_workflow_template = await workflows_helpers.getworkflowbytemplateid(team_id, template_id);
            if (user_workflow_template.length == 0) {
                var workflow_id = randomUUID().replace(/-/g, '');
                await workflows_helpers.createworkflow_from_template(team_id, workflow_id, template_info[0].template_name,
                    template_info[0].template_description, "", template_id);
            }
            else{
                var workflow_id = user_workflow_template[0]["workflow_id"];
            }
            if (status) {
                console.log("Creating WOrklow", workflow_id)
                var template = JSON.parse(JSON.stringify(template_workflows[template_id]));
                console.log("template", template)
                var trigger_details = template[0]
                if (trigger_details["data_mapper"]["platform"] == "FUB") {
                    let trigger_create_resp = await creaateFubTrigger(keys["fub_key"], team_id, trigger_details["data_mapper"]["type"]);
                    console.log("trigger_create_resp", trigger_create_resp)
                    if (trigger_create_resp["statusCode"] != 200) {
                        console.log("Error creating trigger")
                        console.log(keys["fub_key"], keys, trigger_create_resp["data"]["errorMessage"])
    
                        return { "statusCode": 500, "message": trigger_create_resp["data"]["errorMessage"] };
                    }
                    var trigger_id = trigger_create_resp["trigger_id"];
                }
                else{
                    return { "statusCode": 500, "message": "Platform not supported" };
                }
                console.log("trigger_id", trigger_id)
                await workflows_helpers.updateworkflowtrigger(team_id, workflow_id, trigger_id);
    
                trigger_details["data_mapper"]["trigger_id"] = trigger_id;
                // update_actions(workflow_id, trigger_details, context.dynamodbdatabaseloaders);
                template[0] = trigger_details;
                let resp = await setup_fub_for_template(template_id, keys["fub_key"]);
                console.log("resp", resp)
                if (resp["statusCode"] >= 300) {
                    return { "statusCode": 500, "message": resp["data"]["errorMessage"] };
                }
                console.log("Adding actions to table")
                await update_actions(workflow_id, template, context.dynamodbdatabaseloaders); 
            } 
            // could have actually used updateworkflowstatus directly
            var workflows = await workflows_helpers.updateworkflowtemplatestatus(team_id, template_id, status);
            console.log("Done")

            return { "statusCode": 200, "message": "" };
        }
    },

    Trigger: {
        // workflow: (Trigger, args, context, info) => {
        //     console.log("Trigger.Workflows", Trigger, args);
        //     return {workflow_id: Trigger.workflow_id};
        // },
        trigger_id: (Trigger, args, context, info) => {
            // console.log("Trigger.Actions", Trigger, args);
            return Trigger.trigger_id;
        },
        trigger_type: (Trigger, args, context, info) => {
            // console.log("Trigger.Actions", Trigger.trigger_type, args);
            return Trigger.trigger_type;
        },
        status: (Trigger, args, context, info) => {
            // console.log("Trigger.Actions", Trigger, args);
            return Trigger.status;
        },
    },
    Workflow: {
        actions: (workflow, args, context, info) => {
            // console.log("Trigger.Actions", workflow, args);
            var workflow_id = workflow.workflow_id;
            var getactions = () => getactionsbyworkflowid(workflow_id, context.dynamodbdatabaseloaders);
            return getactions();
        },
    },

};