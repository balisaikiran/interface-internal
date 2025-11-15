import { DynamodbLoadersType } from "../modules/database/dynamodb.js";
import { GetItemCommand, QueryCommand, QueryCommandInput, PutItemCommand, UpdateItemCommand, DynamoDBClient, DynamoDBClientConfig, ScanCommandInput, ScanCommand, BatchExecuteStatementCommand, BatchExecuteStatementCommandInput, BatchGetItemCommand, BatchGetItemCommandInput } from "@aws-sdk/client-dynamodb"
import { unmarshall, marshall } from "@aws-sdk/util-dynamodb";

var TriggerTable = process.env.TRIGGER_TABLE
var WORKFLOWS_TABLE = process.env.WORKFLOWS_TABLE
var TriggerEventTable = process.env.TRIGGER_DATA_TABLE
var WorkflowDetailsTable = process.env.WORKFLOW_DETAILS_TABLE
var WORKFLOW_SESSIONS_TABLE = process.env.WORKFLOW_SESSIONS_TABLE

export async function gettriggersbyteamid(team_id: string, dynamodb_loader: DynamodbLoadersType) {
    var _dynamodb_loader = await dynamodb_loader
    var response = await _dynamodb_loader.fulltablequeryloader.load({
        input: {
            TableName: TriggerTable,
            KeyConditionExpression: "team_id = :team_id",
            ExpressionAttributeValues: {
                ":team_id": { S: team_id }
            },
            IndexName: "team_id-index"
        }, num_max_items: -1
    }
    )
    return response.map((item) => unmarshall(item))
}

export async function gettriggerbytriggerid(trigger_id: string, dynamodb_loader: DynamodbLoadersType) {
    var _dynamodb_loader = await dynamodb_loader
    var response = await _dynamodb_loader.fulltablequeryloader.load({
        input: {
            TableName: TriggerTable,
            KeyConditionExpression: "trigger_id = :trigger_id",
            ExpressionAttributeValues: {
                ":trigger_id": { S: trigger_id }
            }
        }, num_max_items: -1
    }
    )
    return response.map((item) => unmarshall(item))
}

export async function getactionsbyworkflowid(workflow_id: string, dynamodb_loader: DynamodbLoadersType) {
    console.log("getactionsbyworkflowid", workflow_id)
    var _dynamodb_loader = await dynamodb_loader
    var response = await _dynamodb_loader.fulltablequeryloader.load({
        input: {
            TableName: WORKFLOWS_TABLE,
            KeyConditionExpression: "workflow_id = :workflow_id",
            ExpressionAttributeValues: {
                ":workflow_id": { S: workflow_id }
            },
            // IndexName: "workflow_id-index"
        }, num_max_items: -1
    }
    )
    console.log("Actions response", response)
    return response.map((item) => unmarshall(item))
}

export function unkown_variable_marshal(variable: any){
    // DO check the variable for null and undefined before calling this function
    // Below check is mostly for recursive calls
    if (variable == null || variable == undefined){
        return marshall(null)
    }
    if (variable.constructor.name == "Object"){
        return { M: marshall(variable) }
    }
    else if (variable.constructor.name == "Array"){
        return { L: variable.map((item) => {
            return unkown_variable_marshal(item)
        }) }
    }
    else if (variable.constructor.name == "String"){
        return { S: variable }
    }
    else if (variable.constructor.name == "Number"){
        return { N: variable.toString() }
    }
    else if (variable.constructor.name == "Boolean"){
        return { BOOL: variable }
    }
    else if (variable.constructor.name == "Set"){
        return { SS: variable }
    }
    else if (variable.constructor.name == "Map"){
        return { M: variable }
    }
    else {
        console.log("unkown_variable_marshal, might break", variable, variable.constructor.name)
        return marshall(variable)
    }
}


export async function updateworkflow_action(workflow_id: string, action_id: string, dynamodb_loader: DynamodbLoadersType,
    action_info: any) {
    console.log("updateworkflow_action", workflow_id, action_id, action_info)

    var _dynamodb_loader = await dynamodb_loader
    // make sure actionumber does not exist for the 
    var ExpressionAttributeValues = {}
    var UpdateExpression = "set "

    const available_keys = ["api_name", "platform", "api_type", "meta_data", "test_status",
                    "automation_name", "data_mapper", "next_action_ids", "is_default"]
    for (let [key, value] of Object.entries(action_info)){
        if (available_keys.includes(key) && value != null && value != undefined && key != "workflow_id" && key != "action_id"){
            ExpressionAttributeValues[":" + key] = unkown_variable_marshal(value)
            if (UpdateExpression.length > 4) {
                UpdateExpression += ", "
            }
            UpdateExpression += key + " = :" + key
        }
    }

    var response = {}
    if (ExpressionAttributeValues){
        console.log("ExpressionAttributeValues", ExpressionAttributeValues)
        console.log("UpdateExpression", UpdateExpression)
        response = await _dynamodb_loader.updateitemloader.load({
            TableName: WORKFLOWS_TABLE,
            Key: {
                "workflow_id": { S: workflow_id },
                "action_id": { S: action_id }
            },
            UpdateExpression: UpdateExpression,
            ExpressionAttributeValues: ExpressionAttributeValues
        }
        )
    }
    return response
}

export async function deleteworkflow_action(workflow_id: string, action_id: string, dynamodb_loader: DynamodbLoadersType) {
    var _dynamodb_loader = await dynamodb_loader
    var response = await _dynamodb_loader.deleteitemloader.load({
        TableName: WORKFLOWS_TABLE,
        Key: {
            "workflow_id": { S: workflow_id },
            "action_id": { S: action_id }
        }
    }
    )
    return response
}

export async function getWorkflowSession(session_id: string, dynamodb_loader: DynamodbLoadersType) {
    try {
        const _dynamodb_loader = await dynamodb_loader;
        // const session_id = `${team_id}-${workflow_id}-test_action`
        const response = await _dynamodb_loader.fulltablequeryloader.load({
            input: {
                TableName: WORKFLOW_SESSIONS_TABLE,
                KeyConditionExpression: 'session_id = :session_id', 
                ExpressionAttributeValues: {
                    ':session_id': { S: session_id },
                },
            },
            num_max_items: -1,
        });

        const unmarshalledSessions = response.map((item) => {
            const unmarshalledItem = unmarshall(item);
            return unmarshalledItem;
        });
        

        return unmarshalledSessions;

    } catch (error) {
        console.error('Error querying sessions:', error);
        throw new Error('Failed to query sessions by workflow');
    }
}

export async function updateworkflow_session(session_id, action_id, dynamodb_loader,
    action_info?: any) {
    var _dynamodb_loader = await dynamodb_loader
    var ExpressionAttributeValues = {}
    var UpdateExpression = ""

    const available_keys = ["action_input", "action_output", "action_status"]
    for (let [key, value] of Object.entries(action_info)){
        if (available_keys.includes(key) && value != null && value != undefined && key != "session_id" && key != "action_id"){
            ExpressionAttributeValues[":" + key] = unkown_variable_marshal(value)
            if (UpdateExpression.length > 0) {
                UpdateExpression += ", "
            }
            UpdateExpression += key + " = :" + key
        }
    }

    var response = {}
    if (ExpressionAttributeValues) {
        console.log("ExpressionAttributeValues", ExpressionAttributeValues)
        console.log("UpdateExpression", UpdateExpression)
        response = await _dynamodb_loader.updateitemloader.load({
            TableName: WORKFLOW_SESSIONS_TABLE,
            Key: {
                "session_id": { S: session_id },
                "action_id": { S: action_id }
            },
            UpdateExpression: UpdateExpression,
            ExpressionAttributeValues: ExpressionAttributeValues,
            // ReturnValues: "ALL_NEW"
        }
        )
    }
    return response
}

// export async function getworkflowdetailsbyworkflowid(workflow_id: string, dynamodb_loader: DynamodbLoadersType) {
//     var _dynamodb_loader = await dynamodb_loader
//     var response = await _dynamodb_loader.fulltablequeryloader.load({
//         input: {
//             TableName: WorkflowDetailsTable,
//             KeyConditionExpression: "workflow_id = :workflow_id",
//             ExpressionAttributeValues: {
//                 ":workflow_id": { S: workflow_id }
//             },
//             // IndexName: "workflow_id-index"
//         }, num_max_items: -1
//     }
//     )
//     return response.map((item) => unmarshall(item))
// }


// export async function gettriggereventsbytriggerid(trigger_id: string, dynamodb_loader: DynamodbLoadersType) {
//     var _dynamodb_loader = await dynamodb_loader
//     var response = await _dynamodb_loader.fulltablequeryloader.load({
//         input: {
//             TableName: TriggerEventTable,
//             KeyConditionExpression: "trigger_id = :trigger_id",
//             ExpressionAttributeValues: {
//                 ":trigger_id": { S: trigger_id }
//             },
//             ScanIndexForward: false,
//             IndexName: "trigger_id-timestamp-index"
//         }, num_max_items: 10
//     }
//     )
//     return response.map((item) => unmarshall(item))
// }

// export async function gettriggereventbytriggeruuid(trigger_uuid: string, dynamodb_loader: DynamodbLoadersType) {
//     var _dynamodb_loader = await dynamodb_loader
//     var response = await _dynamodb_loader.fulltablequeryloader.load({
//         input: {
//             TableName: TriggerEventTable,
//             KeyConditionExpression: "trigger_uuid = :trigger_uuid",
//             ExpressionAttributeValues: {
//                 ":trigger_uuid": { S: trigger_uuid }
//             }
//         }, num_max_items: -1
//     }
//     )
//     return response.map((item) => unmarshall(item))
// }

