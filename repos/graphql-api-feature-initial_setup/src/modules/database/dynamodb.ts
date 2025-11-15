import DataLoader from "dataloader";
import { GetItemCommand, QueryCommand, DeleteItemCommand, DeleteItemCommandInput, QueryCommandInput, PutItemCommand, UpdateItemCommand, UpdateItemCommandInput, DynamoDBClient, ScanCommandInput, ScanCommand } from "@aws-sdk/client-dynamodb"
// const userLoader = new DataLoader(keys => myBatchGetUsers(keys));

var client = new DynamoDBClient({
    region: process.env.REGION
});

async function fulltablequery(query_command_input: QueryCommandInput, num_max_items: number = -1) {

    var response = await client.send(new QueryCommand(query_command_input));
    var items = response.Items;
    var last_evaluated_key = response.LastEvaluatedKey;
    while (last_evaluated_key && (items.length < num_max_items || num_max_items == -1)) {
        query_command_input.ExclusiveStartKey = last_evaluated_key;
        response = await client.send(new QueryCommand(query_command_input));
        items = items.concat(response.Items);
        last_evaluated_key = response.LastEvaluatedKey;
    }
    console.log("Items", items, "LastEvaluatedKey", last_evaluated_key)
    return items;

};

async function fulltablescan(scan_command_input: ScanCommandInput, num_max_items: number = -1) {

    var response = await client.send(new ScanCommand(scan_command_input));
    var items = response.Items;
    var last_evaluated_key = response.LastEvaluatedKey;
    while (last_evaluated_key && (items.length < num_max_items || num_max_items == -1)) {
        scan_command_input.ExclusiveStartKey = last_evaluated_key;
        response = await client.send(new ScanCommand(scan_command_input));
        items = items.concat(response.Items);
        last_evaluated_key = response.LastEvaluatedKey;
    }
    console.log("Items", items, "LastEvaluatedKey", last_evaluated_key)
    return items;

}

async function get_item(get_item_command: GetItemCommand) {
    var response = await client.send(get_item_command);
    return response.Item;
}

async function put_item(put_item_command: PutItemCommand) {
    var response = await client.send(put_item_command);
    return response;
}

async function update_item(update_item_command: UpdateItemCommandInput) {
    var command = new UpdateItemCommand(update_item_command);
    var response = await client.send(command);
    return response;
}

async function delete_item(delete_item_command: DeleteItemCommandInput) {
    var command = new DeleteItemCommand(delete_item_command);
    var response = await client.send(command);
    return response;
}
// Fix all batch functions, they are wrong
// Fine for MVP, but need to fix for production
async function getbatchitems(keys: readonly GetItemCommand[]) {
    // THis function should actually handle batch gets by splitting the keys into batches of 10 and then calling the batch get function
    const items = await Promise.all(keys.map(async (key) => {
        const get_item_command = key as GetItemCommand;
        const item = await get_item(get_item_command);
        return item;
    }));
    return items;
}

async function putbatchitems(keys: readonly PutItemCommand[]) {
    const items = await Promise.all(keys.map(async (key) => {
        const put_item_command = key as PutItemCommand;
        const item = await put_item(put_item_command);
        return item;
    }));
    return items;
}

async function updatebatchitems(keys: readonly UpdateItemCommandInput[]) {
    const items = await Promise.all(keys.map(async (key) => {
        const update_item_command = key as UpdateItemCommandInput;
        const item = await update_item(update_item_command);
        return item;
    }));
    return items;
}

async function deletebatchitems(keys: readonly UpdateItemCommandInput[]) {
    const items = await Promise.all(keys.map(async (key) => {
        const delete_item_command = key as UpdateItemCommandInput;
        const item = await delete_item(delete_item_command);
        return item;
    }));
    return items;
}

async function fulltablequerybatch(keys: readonly {input:QueryCommandInput, num_max_items:number}[]) {
    const items = await Promise.all(keys.map(async (key) => {
        const query_command_input = key.input as QueryCommandInput;
        const num_max_items = key.num_max_items as number;
        const item = await fulltablequery(query_command_input, num_max_items);
        return item;
    }));
    return items;
}
async function fulltablescanbatch(keys: readonly {input:ScanCommandInput, num_max_items:number}[]) {
    const items = await Promise.all(keys.map(async (key) => {
        const scan_command_input = key.input as ScanCommandInput;
        const num_max_items = key.num_max_items as number;
        const item = await fulltablescan(scan_command_input, num_max_items);
        return item;
    }));
    return items;
}


export async function getdynamodbloaders() {
    const getitemloader = new DataLoader((items: GetItemCommand[]) => getbatchitems(items));
    const putitemloader = new DataLoader((items: PutItemCommand[]) => putbatchitems(items));
    const updateitemloader = new DataLoader((items: UpdateItemCommandInput[]) => updatebatchitems(items));
    const fulltablequeryloader = new DataLoader((keys: {input:QueryCommandInput, num_max_items:number}[]) => fulltablequerybatch(keys));
    const fulltablescanloader = new DataLoader((keys: {input:ScanCommandInput, num_max_items:number}[]) => fulltablescanbatch(keys));
    const deleteitemloader = new DataLoader((items: DeleteItemCommandInput[]) => deletebatchitems(items));
    return {
        getitemloader,
        putitemloader,
        updateitemloader,
        fulltablequeryloader,
        fulltablescanloader,
        deleteitemloader
    }
}
export type DynamodbLoadersType = ReturnType<typeof getdynamodbloaders>;