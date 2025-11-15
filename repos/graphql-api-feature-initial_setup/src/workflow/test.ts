import DataLoader from "dataloader";
import { GetItemCommand, QueryCommand, QueryCommandInput, PutItemCommand, UpdateItemCommand, UpdateItemCommandInput, DynamoDBClient, ScanCommandInput, ScanCommand } from "@aws-sdk/client-dynamodb"
// const userLoader = new DataLoader(keys => myBatchGetUsers(keys));
import { marshall } from "@aws-sdk/util-dynamodb";

var client = new DynamoDBClient({
    region: process.env.REGION
});
const WORKFLOW_SESSIONS_TABLE = 'workflow-dev-env-workflowSessions-1ASYMKN00Q5DM'

async function update_item(update_item_command: UpdateItemCommandInput) {
    var command = new UpdateItemCommand(update_item_command);
    var response = await client.send(command);
    return response;
}

async function updatebatchitems(keys: readonly UpdateItemCommandInput[]) {
    const items = await Promise.all(keys.map(async (key) => {
        const update_item_command = key as UpdateItemCommandInput;
        const item = await update_item(update_item_command);
        return item;
    }));
    return items;
}
const updateitemloader = new DataLoader((items: UpdateItemCommandInput[]) => updatebatchitems(items));


const WORKFLOWS_TABLE = 'workflow-dev-env-workflows-TZZNFPQ459ZR'
async function updateworkflow_action(workflow_id: string, action_id: string, dynamodb_loader,
    data_mapper?: any, next_action_id?: string, path?: string) {
    console.log("updateworkflow_action", workflow_id, action_id, data_mapper, next_action_id, path)
    var _dynamodb_loader = await dynamodb_loader
    // make sure actionumber does not exist for the 
    var ExpressionAttributeValues = {}
    var UpdateExpression = ""
    if (data_mapper && Object.keys(data_mapper).length > 0) {
        ExpressionAttributeValues[":data_mapper"] = { M: marshall(data_mapper) }
        UpdateExpression += "set data_mapper = :data_mapper"
    }
    if (next_action_id?.length > 0) {
        ExpressionAttributeValues[":next_action_id"] = marshall(next_action_id)
        if (UpdateExpression.length > 0) {
            UpdateExpression += ", "
        }
        UpdateExpression += "next_action_id = :next_action_id"
    }
    if (path?.length > 0) {
        ExpressionAttributeValues[":path"] = marshall(path)
        if (UpdateExpression.length > 0) {
            UpdateExpression += ", "
        }
        UpdateExpression += "path = :path"
    }
    var response = {}
    if (ExpressionAttributeValues) {
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
    console.log("response", response)
    return response
}

export async function unkown_variable_marshal(variable: any){
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
        console.log("unkown_variable_marshal", variable, variable.constructor.name)
        return marshall(variable)
    }
}    

export async function updateworkflow_session(session_id, action_id, dynamodb_loader,
    action_input?: Record<string, any>, action_output?: any, action_status?: string) {
    var _dynamodb_loader = await dynamodb_loader
    var ExpressionAttributeValues = {}
    var UpdateExpression = ""
    if (action_input && Object.keys(action_input).length > 0) {
        ExpressionAttributeValues[":action_input"] = unkown_variable_marshal(action_input)
        UpdateExpression += "set action_input = :action_input"
    }
    if (action_output != null || action_output != undefined) {
        // console.log("marshall(action_output)", marshall(action_output), typeof action_output, action_output.constructor.name)
        ExpressionAttributeValues[":action_output"] = unkown_variable_marshal(action_output)
        if (UpdateExpression.length > 0) {
            UpdateExpression += ", "
        }
        UpdateExpression += "action_output = :action_output"
    }
    if (action_status && action_status?.length > 0) {
        ExpressionAttributeValues[":action_status"] = unkown_variable_marshal(action_status)
        if (UpdateExpression.length > 0) {
            UpdateExpression += ", "
        }
        UpdateExpression += "action_status = :action_status"
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


// await updateworkflow_action('d2273ca72f7242c28447586a68e7c3a9', 'trigger', { updateitemloader }, { "Test": "Test" }, undefined)
// console.log(await updateworkflow_session('testing_session_id', 'trigger', { updateitemloader }, { "Test": "Test" }, '[{ "Test": "Test"}]'))

console.log(marshall(null))