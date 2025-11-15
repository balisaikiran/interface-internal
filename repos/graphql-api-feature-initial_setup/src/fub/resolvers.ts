import { FubAPI } from "./helper.js";
import { URLSearchParams } from 'url';
import {status_mapping, getstatusstring} from "../modules/helper.js"
import { triggers_helpers } from "../workflow/helper.js";
import {creaateFubTrigger} from "./trigger_helper.js"
const TRIGGER_WEBHOOK_URL = process.env.TRIGGER_WEBHOOK_URL
const getstatus = getstatusstring(status_mapping);

// Write query for every possible type from the types object
export const resolvers = {
    Query: {
        // Generics for all types
        ping: async (_: any, args: any, context: any) => {
            return {"output": "Heyy", "status": "SUCCESS", "info": {}}
        },
        GetFubDataByUrl: async (_: any, args: any, context: any) => {
            var keys = await context.keys.load(context.team_id);
            var keys = JSON.parse(keys);
            var fub = new FubAPI(keys["fub_key"]);
            var response = await fub.get_by_url(args.url);
            return { "output": response.json(), "status": getstatus(response.status) };
        },
        GetFubDataById: async (_: any, args: any, context: any) => {
            var keys = await context.keys.load(context.team_id);
            var keys = JSON.parse(keys);
            var fub = new FubAPI(keys["fub_key"]);
            var type = args.type;
            var id = args.id;
            var params = args.params;
            var response = await fub.get_by_id(type, id, params);
            return { "output": response.json(), "status": getstatus(response.status) };
        },
        GetFubData: async (_: any, args: any, context: any) => {
            var keys = await context.keys.load(context.team_id);
            var keys = JSON.parse(keys);
            var fub = new FubAPI(keys["fub_key"]);
            var type = args.type;
            var params = args.params;
            var response = await fub.get(type, params);
            return { "output": response.json(), "status": getstatus(response.status) };
        },
        GetFubAllData: async (_: any, args: any, context: any) => {
            var keys = await context.keys.load(context.team_id);
            var keys = JSON.parse(keys);
            console.log("GetFubAllData", args, keys["fub_key"], typeof keys)
            var fub = new FubAPI(keys["fub_key"]);
            var type = args.type;
            var response = await fub.get_all_data(type);
            return { "output": response.json(), "status": getstatus(response.status) };
        },
    },
    Mutation: {
        CreateFubResource: async (_: any, args: any, context: any) => {
            var keys = await context.keys.load(context.team_id);
            var keys = JSON.parse(keys);
            var fub = new FubAPI(keys["fub_key"]);
            var type = args.type;
            // Add filter to check if create is allowed for this type
            var data = args.data;
            var response = await fub.post(type, data);
            return { "output": response.json(), "status": getstatus(response.status) };
        },
        UpdateFubResource: async (_: any, args: any, context: any) => {
            var keys = await context.keys.load(context.team_id);
            var keys = JSON.parse(keys);
            var fub = new FubAPI(keys["fub_key"]);
            var type = args.type;
            var id = args.id;
            var data = args.data;
            var params = args.params;
            var response = await fub.put(type, id, data, params);
            return { "output": response.json(), "status": getstatus(response.status) };
        },
        DeleteFubResource: async(_: any, args: any, context: any) => {
            var keys = await context.keys.load(context.team_id);
            var keys = JSON.parse(keys);
            var fub = new FubAPI(keys["fub_key"]);
            var type = args.type;
            var id = args.id;
            var response = await fub.delete(type, id);
            return { "output": response.json(), "status": getstatus(response.status) };
        },
        CheckFubTrigger: async (_: any, args: any, context: any) => {
            var team_id = context.team_id;
            var keys = await context.keys.load(team_id);
            var keys = JSON.parse(keys);
            var fub = new FubAPI(keys["fub_key"]);
            var type = args.type;
            // Check in database if trigger already exists, with team_id, type and platform
            var trigger_id = args.trigger_id;
            if (!trigger_id) {
                return {"data": {"errorMessage": "trigger_id is required"}, "statusCode": 400};
            }
            // get trigger by trigger_id
            // var resp = await pool.query("SELECT * FROM TriggersInfo WHERE trigger_id = $1", [trigger_id]);
            var rows = await triggers_helpers.gettriggerbytriggerid(team_id, trigger_id);
            console.log("resp", rows)
            if (rows.length == 0){
                return {"data": {"errorMessage": "Trigger doesn't exist in System"}, "statusCode": 400};
            }
                // get all webhooks from fub and find the one with the trigger_id
            var response = await fub.get_all_data("webhooks");
            if (response.status >= 300){
                return {"data": response.json(), "statusCode": response.status};
            }
            var webhooks: any = await response.json();
            // find the webhook whose urlparam has the team_id and trigger_id
            var webhook = webhooks.find((webhook: any) => {
                var url = new URL(webhook["url"]);
                var params = new URLSearchParams(url.search);
                return params.get("team_id") == context.team_id && params.get("trigger_id") == trigger_id;
            })
            console.log("webhook", webhook)
            // If webhook doesn't exsist create it
            if (!webhook){
                var data = {
                    "event": type,
                    "url": TRIGGER_WEBHOOK_URL + "?team_id="+ context.team_id + "&trigger_id=" + trigger_id,
                    "status": "Active"
                }
                var response = await fub.post("webhooks", data)
                if (response.status >= 300){
                    return {"data": response.json(), "statusCode": response.status};
                }
            }
            // If webhook status is Disabled, make it Active
            else if (webhook["status"] == "Disabled"){
                var response = await fub.put("webhooks", webhook["id"], {"status": "Active"}, {});
                if (response.status >= 300){
                    return {"data": response.json(), "statusCode": response.status};
                }
            }
            return {"data": {}, "statusCode": 200};
        },
        CreateFubTrigger: async (_: any, args: any, context: any) => {
            console.log("CreateFubTrigger team_id", context.team_id)
            let _keys = await context.keys.load(context.team_id);
            let keys = JSON.parse(_keys);
            let team_id = context.team_id;
            console.log("keys", keys, typeof keys)
            return creaateFubTrigger(keys["fub_key"], team_id, args.type);
            // will have to pass account id for supporting multiple accounts in single team
            // var account_id = args.account_id;
            // if (!account_id){
            //     account_id = 'default'
            // }
        }
    }
}