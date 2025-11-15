// Below are reasons for using such a schema. If anything changes in the future you can remove the JSON type/use fub_full_schema.js
// 1. We always pull entire data from a given API hence by using this we avoid write complex/long queries
// 2. We don't do any filtering on the data fetched all of it is done in a different step in the automation builder system.
// 3. We have followed zapiers approach where it fetches all the info and then lets yyou filter.
// 4. Any addition of fields in these API's will have us changing quries in both frontend and backend of the automation builder
// 5. FUB deal custom fields and fub person custom fields have to be declared in a seperate field called custom_field

// Problems with this JSON type as of now, problems may increase, accordingly you can change
// 1. If we have types defined in here, we could just easily show all possible fields in UI even before API fetch runs
// 2. Same could be done for mutations as well

// The above 2 problems can easily be handled by hardcoding on the UI end itself, instead of scehma, hence we are using JSON type

export const typeDef = `#graphql
  scalar GraphQLJSON

type FubTriggger implements Response {
  statusCode: Int!
  message: String
  data: GraphQLJSON
  trigger_id: String
}

type ActionResponse {
  output: GraphQLJSON!
  status: String!
  info: GraphQLJSON
}

type Query {
    GetFubDataByUrl(url: String!): ActionResponse!
    GetFubDataById(type: String!, id: String!, params: GraphQLJSON): ActionResponse!
    GetFubData(type: String!, params: GraphQLJSON): ActionResponse!
    GetFubAllData(type: String!): ActionResponse!
    ping: ActionResponse!
}

type Mutation {
    CreateFubResource(type: String!, data: GraphQLJSON!): ActionResponse!
    UpdateFubResource(type: String!, id: String!, data: GraphQLJSON!, params: GraphQLJSON): ActionResponse!
    DeleteFubResource(type: String!, id: String!): ActionResponse!
    # Functions called by fornend
    CreateFubTrigger(type: String!): FubTriggger!
    CheckFubTrigger(type: String!, trigger_id: String!): APIResponse!
}
`;


// GetPersonById(id: String!): APIResponse!
// GetPeople(params: GraphQLJSON): APIResponse!
// GetNoteById(id: String!): APIResponse!
// GetNotes(params: GraphQLJSON): APIResponse!
// GetNotesByPersonId(personId: String!, params: GraphQLJSON): APIResponse!
// GetPipelineById(id: String!): APIResponse!
// GetPipelineByName(name: String!): APIResponse!
// GetDealById(id: String!): APIResponse!
// GetDeals(params: GraphQLJSON): APIResponse!
// GetDealsByPersonId(personId: String!, params: GraphQLJSON): APIResponse!
// GetUserById(id: String!): APIResponse!
// GetUsers(params: GraphQLJSON): APIResponse!
// GetCallById(id: String!): APIResponse!
// GetCalls(params: GraphQLJSON): APIResponse!
// GetCallsByPersonId(personId: String!, params: GraphQLJSON): APIResponse!
// GetTaskById(id: String!): APIResponse!
// GetTasks(params: GraphQLJSON): APIResponse!
// GetTasksByPersonId(personId: String!, params: GraphQLJSON): APIResponse!
// GetWebhookById(id: String!): APIResponse!
// GetWebhooks(params: GraphQLJSON): APIResponse!
// GetTextMessageById(id: String!): APIResponse!
// GetTextMessages(params: GraphQLJSON): APIResponse!
// GetTextMessagesByPersonId(personId: String!, params: GraphQLJSON): APIResponse!
// GetEmailById(id: String!): APIResponse!
// GetEmails(params: GraphQLJSON): APIResponse!
// GetAppointmentById(id: String!): APIResponse!
// GetAppointments(params: GraphQLJSON): APIResponse!
// GetAppointmentsByPersonId(personId: String!, params: GraphQLJSON): APIResponse!
// GetAppointmentTypeById(id: String!): APIResponse!
// GetAppointmentTypes(params: GraphQLJSON): APIResponse!
// GetAppointmentOutcomeById(id: String!): APIResponse!
// GetAppointmentOutcomes(params: GraphQLJSON): APIResponse!
// GetActionPlansPersonById(id: String!): APIResponse!
// GetActionPlans(params: GraphQLJSON): APIResponse!
// GetActionPlansByPersonId(personId: String!, params: GraphQLJSON): APIResponse!
// GetSmartListById(id: String!): APIResponse!
// GetSmartLists(params: GraphQLJSON): APIResponse!
// GetPeopleRelationshipById(id: String!): APIResponse!
// GetPeopleRelationships(params: GraphQLJSON): APIResponse!
// GetPeopleRelationshipsByPersonId(personId: String!, params: GraphQLJSON): APIResponse!
// GetPondById(id: String!): APIResponse!
// GetPonds(params: GraphQLJSON): APIResponse!
// GetCustomFieldById(id: String!): APIResponse!
// GetCustomFields(params: GraphQLJSON): APIResponse!
