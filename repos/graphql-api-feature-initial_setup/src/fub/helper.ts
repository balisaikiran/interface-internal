import fetch, { Response } from "node-fetch";
import { URLSearchParams } from 'url';

// declare global {
//     var fetch: typeof import("node-fetch").default;
//   }

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
export class FubAPI {
    baseURL = "https://api.followupboss.com/v1/";
    private token: string;
    private headers;
    private types = {
        "people": this.baseURL + "people",
        "notes": this.baseURL + "notes",
        "pipelines": this.baseURL + "pipelines",
        "deals": this.baseURL + "deals",
        "users": this.baseURL + "users",
        "calls": this.baseURL + "calls",
        "tasks": this.baseURL + "tasks",
        "webhooks": this.baseURL + "webhooks",
        "textMessages": this.baseURL + "textMessages",
        "emails": this.baseURL + "emails",
        "appointments": this.baseURL + "appointments",
        "appointmenttypes": this.baseURL + "appointmentTypes",
        "appointmentoutcomes": this.baseURL + "appointmentOutcomes",
        "actionPlansPeople": this.baseURL + "actionPlansPeople",
        "actionPlans": this.baseURL + "actionPlans",
        "smartLists": this.baseURL + "smartLists",
        "peopleRelationships": this.baseURL + "peopleRelationships",
        "customfields": this.baseURL + "customFields",
        // just a small thing to notice, key and value are different here
        "dealcustomfields": this.baseURL + "dealCustomFields",
        "ponds": this.baseURL + "ponds",
        "stages": this.baseURL + "stages",
    }
    constructor(fub_key: string) {
        this.token = Buffer.from(String(fub_key) + ":").toString('base64')
        // console.log("fub_key", this.token)
        this.headers = {
                "Authorization": "Basic " + this.token, // this.token,
                "content-type": "application/json",
                "Accept": "text/plain",
                "X-System": "InterFace",
                "X-System-Key": "b0c557612c52720182b4fd0b4051685c",

            }
        this._get_all_data = this._get_all_data.bind(this);
        this._get_by_id = this._get_by_id.bind(this);
        this._get_by_url = this._get_by_url.bind(this);
        this._post = this._post.bind(this);
        this._put = this._put.bind(this);
        this.get_by_id = this.get_by_id.bind(this);
        this.get_all_data = this.get_all_data.bind(this);
        this.post = this.post.bind(this);
        this.put = this.put.bind(this);
        this.get_by_url = this.get_by_url.bind(this);
        this.retry = this.retry.bind(this);
    }

    // Function inspired from https://tusharf5.com/posts/type-safe-retry-function-in-typescript/
    async retry<T extends (...arg0: any[]) => any>(
        fn: T,
        args: Parameters<T>,
        maxTry: number,
        retryCount = 1
    ): Promise<Response> {
        var response: Response;
        try {
            response = (await fn(...args)) as Response;
            if (response.status == 429) {
                if (retryCount < maxTry) {
                    await sleep(1000);
                    return this.retry(fn, args, maxTry, retryCount + 1);
                }
            }
        } catch (error) {
            response = new Response(JSON.stringify(error), { status: 500 });
        }
        return response;
    }

    private async _get_by_id(type: string, id: string = "", params: any = {}): Promise<Response> {
        let url = this.types[type];
        if (id !== "" && id !== undefined && id !== null) {
            url += "/" + id;
        }
        const response = await this._get_by_url(url + "?" + new URLSearchParams(params).toString());

        return response;
    }

    private async _get_by_url(url: string): Promise<Response> {
        const response = await fetch(url, {
            headers: this.headers,
            method: "GET",
        });
        return response;
    }

    private async _get_all_data(type: string): Promise<Response> {
        let params = {};
        const limit_per_request = 100;
        params["limit"] = limit_per_request;
        params["offset"] = 0;
        console.log("this.types", this.types)
        let url = this.types[type] + "?" + new URLSearchParams(params).toString();
        let fub_data_list = [];
        let fub_data;
        let completed = false;
        while (!completed) {
            // const fub_data = await this._get_by_url(url);
            fub_data = await this.retry(this._get_by_url, [url], 5);
            if (fub_data.status >= 300) {
                return fub_data;
            }
            fub_data = await fub_data.json();
            console.log("fub_data", fub_data)
            fub_data_list.push(...fub_data[type]);
            if (fub_data[type].length < limit_per_request) {
                completed = true;
            } else {
                url = fub_data["_metadata"]["nextLink"];
                if (!url) {
                    completed = true;
                }
                console.log("url", url)
            }
        }
        var data = new Response(JSON.stringify(fub_data_list), { status: 200 });
        return data
    }

    private async _post(type: string, data: any): Promise<Response> {
        const response = await fetch(this.types[type], {
            method: "POST",
            headers: this.headers,
            body: JSON.stringify(data),
        });
        return response;
    }

    private async _put(type: string, id: string, data: any, params:any): Promise<Response> {
        const response = await fetch(this.types[type] + "/" + id + "?" + new URLSearchParams(params || {}).toString(), {
            method: "PUT",
            headers: this.headers,
            body: JSON.stringify(data),
        });
        return response;
    }

    private async _delete(type: string, id: string): Promise<Response> {
        const response = await fetch(this.types[type] + "/" + id, {
            method: "DELETE",
            headers: this.headers,
        });
        return response;
    }

    async get_by_id(type: string, id: string = "", params: any = {}) {
        if (!(type in this.types)) {
            return new Response(JSON.stringify({ "error": `Get type: ${type} not supported` }), { status: 400 });
        }
        return this.retry(this._get_by_id, [type, id, params], 5);
    }
    
    async get(type: string, params: any = {}) {
        if (!(type in this.types)) {
            return new Response(JSON.stringify({ "error": `Get type: ${type} not supported` }), { status: 400 });
        }
        return this.retry(this._get_by_id, [type, "", params], 5);
    }

    async get_by_url(url: string) {
        return await this.retry(this._get_by_url, [url], 5);
    }

    async get_all_data(type: string) {
        if (!(type in this.types)) {
            return new Response(JSON.stringify({ "error": `Get type: ${type} not supported` }), { status: 400 });
        }
        // Because of the way the API is designed, we need to make multiple requests to get all the data
        // This function will make all the requests and return a single list of data
        return await this._get_all_data(type);
    }

    async post(type: string, data: any) {
        if (!(type in this.types)) {
            return new Response(JSON.stringify({ "error":`Post type: ${type} not supported` }), { status: 400 });
        }
        return await this.retry(this._post, [type, data], 5);
    }

    async put(type: string, id: string, data: any, params: any) {
        if (!(type in this.types)) {
            return new Response(JSON.stringify({ "error": `Put type: ${type} not supported` }), { status: 400 });
        }
        return await this.retry(this._put, [type, id, data, params], 5);
    }

    async delete(type: string, id: string) {
        if (!(type in this.types)) {
            return new Response(JSON.stringify({ "error": `Delete type: ${type} not supported`  }), { status: 400 });
        }
        return await this.retry(this._delete, [type, id], 5);
    }

}
