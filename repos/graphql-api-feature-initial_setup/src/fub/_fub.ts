import { FubAPI } from "./helper.js";
// File not used
export const resolvers = {
    Query: {
        // people
        GetPersonById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var params = {"fields": "allFields"}
            var response = await fub.get_by_id("people", args.id, params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetPeople: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get("people", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // note
        GetNoteById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_id("notes", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetNotes: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get("notes", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetNotesByPersonId: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var params = args.params;
            // later can change with get_all_data
            params["personId"] = args.personId;
            var response = await fub.get("notes", params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // pipeline
        GetPipelineById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var response = await fub.get_by_id("pipelines", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetPipelineByName: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var params = {"name": args.name};
            var response = await fub.get("pipelines", params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // deal
        GetDealById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var response = await fub.get_by_id("deals", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetDeals: async(_: any, args: any, context: any) => {
            // Can get deal by pipelineid, userid, and personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            // later can change with get_all_data
            var response = await fub.get("deals", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetDealsByPersonId: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var params = args.params;
            // later can change with get_all_data
            params["personId"] = args.personId;
            var response = await fub.get("deals", params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // user
        GetUserById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var response = await fub.get_by_id("users", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetUsers: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            // later can change with get_all_data
            var response = await fub.get("users", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetUserByName: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            // later can change with get_all_data
            var firstname = args.firstname.toLowerCase().trim();
            var lastname = args.lastname.toLowerCase().trim();
            var fullname = firstname + " " + lastname;
            var response = await fub.get_all_data("users");
            var users: any = await response.json();
            var user = users.find((user: any) => {
                var user_fullname = user["firstName"].toLowerCase().trim() + " " + user["lastName"].toLowerCase().trim();
                return user_fullname === fullname;
            });

            return {"data": user[0], "statusCode": response.status};
        },
        // calls
        GetCallById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var response = await fub.get_by_id("calls", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetCalls: async(_: any, args: any, context: any) => {
            // Can get call by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            // later can change with get_all_data
            var response = await fub.get("calls", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetCallsByPersonId: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var params = args.params;
            // later can change with get_all_data
            params["personId"] = args.personId;
            var response = await fub.get("calls", params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // tasks
        GetTaskById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_id("tasks", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetTasks: async(_: any, args: any, context: any) => {
            // Can get task by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get("tasks", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetTasksByPersonId: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var params = args.params;
            // later can change with get_all_data
            params["personId"] = args.personId;
            var response = await fub.get("tasks", params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // webhooks
        GetWebhookById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_id("webhooks", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetWebhooks: async(_: any, args: any, context: any) => {
            // Can get webhook by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get("webhooks", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // textMessages
        GetTextMessageById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_id("textMessages", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetTextMessages: async(_: any, args: any, context: any) => {
            // Can get textMessage by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get("textMessages", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetTextMessagesByPersonId: async(_: any, args: any, context: any) => {
            // Can get textMessage by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var params = args.params;
            // later can change with get_all_data
            params["personId"] = args.personId;
            var response = await fub.get("textMessages", params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // emails
        GetEmailById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var response = await fub.get_by_id("emails", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        // Appointments
        GetAppointmentById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var response = await fub.get_by_id("appointments", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetAppointments: async(_: any, args: any, context: any) => {
            // Can get appointment by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            // later can change with get_all_data
            var response = await fub.get("appointments", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetAppointmentsByPersonId: async(_: any, args: any, context: any) => {
            // Can get appointment by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var params = args.params;
            // later can change with get_all_data
            params["personId"] = args.personId;
            var response = await fub.get("appointments", params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // appointmentTypes
        GetAppointmentTypeById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            var response = await fub.get_by_id("appointmentTypes", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetAppointmentTypes: async(_: any, args: any, context: any) => {
            // Can get appointmentType by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key); 
            // later can change with get_all_data
            var response = await fub.get_all_data("appointmentTypes");
            return {"data": response.json(), "statusCode": response.status};
        },
        // appointmentOutcomes
        GetAppointmentOutcomeById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_id("appointmentOutcomes", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetAppointmentOutcomes: async(_: any, args: any, context: any) => {
            // Can get appointmentOutcome by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get_all_data("appointmentOutcomes");
            return {"data": response.json(), "statusCode": response.status};
        },
        // actionPlansPeople
        GetActionPlansPersonById: async(_: any, args: any, context: any) => {
            // Can get actionPlansPerson by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_id("actionPlansPeople", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetActionPlans: async(_: any, args: any, context: any) => {
            // Can get actionPlansPerson by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get("actionPlansPeople", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetActionPlansByPersonId: async(_: any, args: any, context: any) => {
            // Can get actionPlansPerson by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var params = args.params;
            // later can change with get_all_data
            params["personId"] = args.personId;
            var response = await fub.get("actionPlansPeople", params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // smartLists
        GetSmartListById: async(_: any, args: any, context: any) => {
            // Can get smartList by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_id("smartLists", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetSmartLists: async(_: any, args: any, context: any) => {
            // Can get smartList by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get_all_data("smartLists");
            return {"data": response.json(), "statusCode": response.status};
        },
        // peopleRelationships
        GetPeopleRelationshipById: async(_: any, args: any, context: any) => {
            // Can get peopleRelationship by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_id("peopleRelationships", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetPeopleRelationships: async(_: any, args: any, context: any) => {
            // Can get peopleRelationship by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get("peopleRelationships", args.params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetPeopleRelationshipsByPersonId: async(_: any, args: any, context: any) => {
            // Can get peopleRelationship by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var params = args.params;
            // later can change with get_all_data
            params["personId"] = args.personId;
            var response = await fub.get("peopleRelationships", params);
            return {"data": response.json(), "statusCode": response.status};
        },
        // customFields
        // GetCustomFieldById: async(_: any, args: any, context: any) => {
        //     // Can get customField by personid
        //     var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
        //     var response = await fub.get_by_id("customFields", args.id);
        //     return {"data": response.json(), "statusCode": response.status};
        // },
        // ponds
        GetPondById: async(_: any, args: any, context: any) => {
            // Can get pond by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_id("ponds", args.id);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetPonds: async(_: any, args: any, context: any) => {
            // Can get pond by personid
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            // later can change with get_all_data
            var response = await fub.get_all_data("ponds");
            return {"data": response.json(), "statusCode": response.status};
        },
        // Generics for all types
        GetFubDataByUrl: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var response = await fub.get_by_url(args.url);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetFubDataById: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var type = args.type;
            var id = args.id;
            var params = args.params;
            var response = await fub.get_by_id(type, id, params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetFubData: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var type = args.type;
            var params = args.params;
            var response = await fub.get(type, params);
            return {"data": response.json(), "statusCode": response.status};
        },
        GetFubAllData: async(_: any, args: any, context: any) => {
            var fub = new FubAPI(context.keys.load(args.team_id).fub_key);
            var type = args.type;
            var response = await fub.get_all_data(type);
            return {"data": response.json(), "statusCode": response.status};
        }
    },
    Mutation: {
        UpdatePeople: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var data = args.data;
            var response = await fub.put("people", args.id, data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreatePeople: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var data = args.data;
            var response = await fub.post("people", data);
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateNotes: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var data = args.data;
            var response = await fub.post("notes", data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateNotes: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var data = args.data;
            var response = await fub.put("notes", args.id, data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateDeals: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var data = args.data;
            var response = await fub.post("deals", data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateDeals: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var data = args.data;
            var response = await fub.put("deals", args.id, data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateCalls: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // var data = args.data;
            var response = await fub.post("calls", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateCalls: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // var data = args.data;
            var response = await fub.put("calls", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateTasks: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // var data = args.data;
            var response = await fub.post("tasks", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateTasks: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // var data = args.data;
            var response = await fub.put("tasks", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateWebhooks: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // var data = args.data;
            var response = await fub.post("webhooks", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateWebhooks: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // var data = args.data;
            var response = await fub.put("webhooks", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateTextMessages: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // var data = args.data;
            var response = await fub.post("textMessages", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateTextMessages: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // var data = args.data;
            var response = await fub.put("textMessages", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateEmails: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.post("emails", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateEmails: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.put("emails", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateAppointments: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.post("appointments", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateAppointments: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.put("appointments", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateAppointmentTypes: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.post("appointmenttypes", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateAppointmentTypes: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.put("appointmenttypes", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateAppointmentOutcomes: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.post("appointmentoutcomes", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateAppointmentOutcomes: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.put("appointmentoutcomes", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateActionPlansPeople: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.post("actionPlansPeople", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateActionPlansPeople: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.put("actionPlansPeople", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateSmartLists: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.post("smartLists", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateSmartLists: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.put("smartLists", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreatePeopleRelationships: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            var response = await fub.post("peopleRelationships", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdatePeopleRelationships: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // var data = args.data;
            var response = await fub.put("peopleRelationships", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateCustomFields: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // console.log("args.data", args.data)
            var response = await fub.post("customFields", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateCustomFields: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // console.log("args.data", args.data)
            var response = await fub.put("customFields", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
        CreateDealCustomFields: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // console.log("args.data", args.data)
            var response = await fub.post("dealcustomfields", args.data);
            return {"data": response.json(), "statusCode": response.status};
        },
        UpdateDealCustomFields: async (_: any, args: any, context: any) => {
            var fub = new FubAPI(context.fub_key);
            // console.log("args.data", args.data)
            var response = await fub.put("dealcustomfields", args.id, args.data, {});
            return {"data": response.json(), "statusCode": response.status};
        },
}
}