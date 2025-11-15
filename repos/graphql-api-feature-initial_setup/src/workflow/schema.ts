export const typeDef = `#graphql

scalar GraphQLJSON
type Trigger {
  trigger_id: ID!
  trigger_type: String
  team_id: String!
  status: Boolean
  auth: String
}

type TriggerEvent {
  trigger_id: String
  trigger_uuid: ID!
  event_data: GraphQLJSON
  timestamp: String
}

type TestTrigger{
event_data: GraphQLJSON
session_id: String
trigger_id: String
trigger_uuid: String
}

type Action {
  action_id: ID!
  next_action_ids: [String]
  next_acion_id: String
  meta_data: GraphQLJSON
  data_mapper: GraphQLJSON
  action_path: String
  api_name: String
  api_type: String
  automation_name: String
  test_status: String
  is_default: Boolean
  platform: String
}

type Workflow {
  actions: [Action]
  workflow_name: String
  workflow_description: String
  workflow_id: ID!
  trigger_id: ID
  status: Boolean
}

type ActionInfo{
  attempt_count: Int
  error: GraphQLJSON
}

type ActionData {
  action_id: ID!
  action_status: String
  LastUpdatetime: String
  action_info: ActionInfo
  action_input: GraphQLJSON
  action_output: GraphQLJSON
}

type WorkflowSession {
  session_id: ID!
  action_id: ID!
  action_status: String
  LastUpdatetime: String
  action_info: ActionInfo
  action_input: GraphQLJSON
  action_output: GraphQLJSON
}

type TriggerTypes{
  data: GraphQLJSON
  statusCode: Int!
}
#type TriggerTypes{
#  platform: String
#  name: String
#  description: String
#  type: String
#}
interface Response {
    statusCode: Int!
  message: String  # Not populated for now
  data: GraphQLJSON
}

type APIResponse implements Response {
    statusCode: Int!
  message: String  # Not populated for now
  data: GraphQLJSON
}

type WorkflowTemplate {
  template_id: ID!
  template_name: String
  template_description: String
  status: Boolean
}


type Query {
  # Trigger(trigger_id: String!): Trigger,  # Get Trigger info by trigger_id
  # Triggers(team_id: String!): [Trigger],  # Get all Triggers for a team
  TriggerEvent(trigger_uuid: String!): TriggerEvent, # Get TriggerEvent info by trigger_uuid
  TriggerEvents(trigger_id: String!): [TriggerEvent], # Get all TriggerEvents for a trigger
  TestTrigger(trigger_id: String!): TestTrigger, # Select a testing trigger for a workflow
  # Could not write the return type in schema for the below function, so returning GraphQLJSON
  GetAvailableTriggers: TriggerTypes, # Get all available trigger types for a team

  Workflow(workflow_id: String!): Workflow, # Get Workflow info by workflow_id
  Workflows: [Workflow], # Get all Workflows for a team
  WorkflowSession(session_id: String!): WorkflowSession, # Get WorkflowSession info by session_id
  TestSession(workflow_id: String!): APIResponse, # Get WorkflowSession info by session_id
  WorkflowSessions(workflow_id: String!): [WorkflowSession], # Get all WorkflowSessions for a workflow
  GetTemplates: [WorkflowTemplate], # Get all templates for a team
}

type Mutation {
CreateWorkflow(workflow_name: String!, workflow_description: String!): Workflow, # Create a new Workflow
UpdateWorkflowDetails(workflow_id: String!, workflow_name: String, workflow_description: String): APIResponse, # Update Workflow details
UpdateWorkflowTrigger(workflow_id: String!, trigger_data: GraphQLJSON!): APIResponse,
UpdateWorkflowActions(workflow_id: String!, actions_info: GraphQLJSON!): APIResponse,
UpdateSession(workflow_id: String!, session_id: String!): APIResponse,
UpdateWorkflowStatus(workflow_id: String!, status: Boolean!): APIResponse,
UpdateWorkflowTemplateStatus(template_id: String!, status: Boolean!): APIResponse,
}
`
// type Mutation: {

//   CreateTrigger(type: String!, platform:  String!): Trigger, # Create a new Trigger
// },
// TriggerEvent(trigger_id: String!, trigger_uuid: String!): TriggerEvent,
// interface DataMapper {
//   test: String
//   }
  
//   type condition {
//   _data_type: String
//   _expected_value: String
//   _operator: String
//   _value: String
//   }

//   type condition_data_mapper implements DataMapper {
//       test: String
//       mapper: [[condition]]
//   }