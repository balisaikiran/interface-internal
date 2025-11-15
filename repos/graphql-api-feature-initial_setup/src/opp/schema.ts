export const typeDef = `#graphql
scalar GraphQLJSON

type Opp {
  opp_key: String!
  sisu_client_updated_ts: String
  opp_updated_ts: String
  opp_stage: String
  opp_agreement_signed_date: String
  fub_deal_created_ts: String
  opp_type: String
  opp_appt_date: String
  fub_deal_stage_name: String
  opp_appt_met_date: String
  fub_person_id: String
  sisu_client_created_ts: String
  opp_created_ts: String
  fub_deal_id: String
  opp_appt_disposition: String
  teamFubDealId: String
  team: String!
  fub_deal_entered_stage_ts: String
  sisu_client_id: String
  opp_assigned_osa: String
  opp_isa: String
  opp_notes: String
  opp_address: String
  opp_agreement_expiration_date: String
  appt_set_entry_id: String
  fub_appt_start_time: String
  fub_original_appt_start_time: String
  disp_text_wait_timestamp: String
  appt_set_lead_type: String
  appt_set_platform: String
  disp_text_original_wait_timestamp: String
  opp_address2: String
  opp_city: String
  opp_postal_code: String
  opp_last_name: String
  opp_state: String
  previous_opp_stage: String
  CreateEntryId: String
  pipeline_entry_id: String
  opp_forecasted_close_date: String
  opp_under_contract_date: String
  appt_form_id: String
  form_id_entry_id: String
  opp_settlement_date: String
  CreateFormId: String
  appt_outcome: String
  external_system_key_buyer: String
  otc_property_id: String
  external_system_key_seller: String
  FormId_EntryIds: [String]
  opp_price: Float
  opp_commission_percent: Float
  fub_appt_id: String
  custom_fields: GraphQLJSON
  form_entries: [formEntry]
  
}


type formEntry {
  form_entry_id: String!
  form_id: String!
  form_entry_data: GraphQLJSON
  entry_created_date: String
}

type formData {
  form_id: String!
  team_id: String!
  form_name: String
  form_description: String
  form_fields: GraphQLJSON
  form_conditions: GraphQLJSON
  status: Boolean
  form_created_date: String
  form_updated_date: String
  update_by: String
  base_form_template: String
  color_scheme: String
  logo_url: String
  form_type: String
}

type formNamesData {
  form_id: String!
  form_name: String
}

type formResponsePayload {
  team_id: String!
  form_id: String
}

type createFormPayload {
  form_id: String!
  form_entry_id: String!
  entry_created_date: String
}

type customFieldPayload {
  field_id: String!
  field_name: String
  field_description: String
  field_type: String
  settings: GraphQLJSON
  linked_to: String
}

type customFieldResponse {
  field_id: String!
}

type count_value {
  count: String
}

type fieldData {
  field_id: String!
  field_name: String
  field_type: String
  input_type: String
  settings: GraphQLJSON
}

type fieldResponsePayload {
  field_id: String!
  field_name: String
  field_description: String
  field_type: String
  settings: GraphQLJSON
}

type fieldCreatePayload {
  field_id: String!
}

type OppMutationResponse {
  opp_key: String!
}

type Query {
    Opps: [Opp]
    opportunity(opp_key: String): Opp
    opportunitiesByPersonId(team_id: String, fub_person_id: String): [Opp]

    formEntries(form_id: String): [formEntry]
    formEntry(form_entry_id: String): formEntry
    countFormEntries(form_id: String): count_value
    countFormEntriesToday(form_id: String): count_value

    forms(offset: String): [formData]
    formsNames(team_id: String): [formNamesData]
    formData(form_id: String): formData
    countTotalForms: count_value

    GetFormFields(form_id: String): [fieldData]
    GetFieldsByTeamId: [fieldData]
    GetFieldById(field_id: String): fieldData

    GetCustomFields: [customFieldPayload]
  }
  
type Mutation {
    CreateForm(form_data: GraphQLJSON): formResponsePayload
    UpdateForm(form_id: String, form_data: GraphQLJSON): formResponsePayload
    UpdateFormName(form_id: String, form_name: String): formResponsePayload
    DeleteForm(form_id: String): formResponsePayload
    DuplicateForm(form_id: String): formData
    
    CreateFormEntry(form_id: String, form_entry_data: GraphQLJSON): createFormPayload
    UpdateFormEntry(form_id: String, form_entry_id: String, form_entry_data: GraphQLJSON): createFormPayload
    DeleteFormEntry(form_id: String, form_entry_id: String): createFormPayload
    
    CreateField(field_data: GraphQLJSON): fieldCreatePayload
    UpdateField(field_id: String, field_data: GraphQLJSON): fieldCreatePayload

    CreateCustomField(custom_fields: GraphQLJSON): customFieldResponse

    CreateOpp(form_id: String, opp_data: GraphQLJSON): OppMutationResponse
    UpdateOpp(form_id: String, opp_key: String, opp_data: GraphQLJSON): OppMutationResponse
    
  }`
  
  
  // countFormEntriesDate(form_id: String, date: String): count_value
  
  // DeleteOpp(opp_key: String): Opp
//  Opp(opp_key: String): Opp
// Opp(team: String, fub_deal_id: String): Opp
// Opp(team: String, sisu_cliend_id: String): Opp
// Opp(form_id_entry_id: String): Opp
// Opp(team: String, otc_property_id: String): Opp


