import { triggers_types as fub_triggers_types } from "./triggers.js";
import { FubAPI } from "./helper.js";
import { pool } from "../modules/database/pg.js";
import { randomUUID } from 'crypto';
import { triggers_helpers } from "../workflow/helper.js";
const TRIGGER_WEBHOOK_URL = process.env.TRIGGER_WEBHOOK_URL

export const creaateFubTrigger = async (fub_key, team_id, type) => {
    console.log("fub_key:", fub_key)
    var fub = new FubAPI(fub_key);
    console.log("CreateFubTrigger types", type, fub_triggers_types)
    if (!fub_triggers_types.includes(type)) {
        console.log("Trigger type not supported")
        return { "data": { "errorMessage": "Trigger type not supported" }, "statusCode": 400 };
    }
    // Check in database if trigger already exists, with team_id, type and platform, if already exsists get the trigger id
    // var resp = await pool.query("SELECT * FROM TriggersInfo WHERE team_id = $1 AND type = $2 AND platform = $3", [context.team_id, type, "FUB"]);
    // Will have to add account_id parameter for supporting multiple accounts in single team
    console.log("CreateFubTrigger query", team_id, "FUB", type)
    var rows = await triggers_helpers.gettriggerbyteamidandtype(team_id, "FUB", type);
    console.log("CreateFubTrigger resp", rows)
    if (rows.length > 0) {
        let trigger_id = rows[0]["trigger_id"];
        // Get all webhooks from fub and find the trigger with trigger_id and team_id, if status is Disabled , change status to Active
        var response = await fub.get_all_data("webhooks");
        var webhooks: any = await response.json();
        console.log("webhooks: ", webhooks, response.status)
        if (response.status >= 300) {
            console.log("Error getting webhooks")
            return { "data": webhooks, "statusCode": response.status };
        }
        // find the webhook whose urlparam has the team_id and trigger_id
        var webhook = webhooks.find((webhook: any) => {
            var url = new URL(webhook["url"]);
            var params = new URLSearchParams(url.search);
            return params.get("team_id") == team_id && params.get("trigger_id") == trigger_id;
        })
        console.log("webhook", webhook)
        // If webhook doesn't exsist create it
        if (!webhook) {
            var data = {
                "event": type,
                "url": TRIGGER_WEBHOOK_URL + "?team_id=" + team_id + "&trigger_id=" + trigger_id,
                "status": "Active"
            }
            var response = await fub.post("webhooks", data)
            let createwebhookresp = await response.json();
            if (response.status >= 300) {
                return { "data": createwebhookresp, "statusCode": response.status };
            }
        }
        // If webhook status is Disabled, make it Active
        else if (webhook["status"] == "Disabled") {
            var response = await fub.put("webhooks", webhook["id"], { "status": "Active" }, {});
            let updatewebhookresp = await response.json();
            if (response.status >= 300) {
                return { "data": updatewebhookresp, "statusCode": response.status };
            }
        }
        return { "data": {}, "message": "Trigger Already Exists", "trigger_id": trigger_id, "statusCode": 200 };
    }

    // create random uuid for trigger_id, and remove dashes
    var trigger_id = randomUUID().replace(/-/g, '');
    // using same client for transactions
    const client = await pool.connect();
    // start transaction

    await client.query('BEGIN');
    await client.query("INSERT INTO TriggersInfo (trigger_id, platform, type, team_id) VALUES ($1, $2, $3, $4)", [trigger_id, "FUB", type, team_id])
    var data = {
        "event": type,
        "url": TRIGGER_WEBHOOK_URL + "?team_id=" + team_id + "&trigger_id=" + trigger_id,
        "status": "Active"
    }
    var response = await fub.post("webhooks", data)

    if (response.status >= 300) {
        await client.query('ROLLBACK');
        console.log("Error creating webhook")
        trigger_id = null;
    }
    else {
        await client.query('COMMIT');
    }
    client.release()
    var resp = await response.json();
    console.log("response", resp)
    return { "data": resp, "statusCode": response.status, trigger_id: trigger_id };
}
