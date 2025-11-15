// We are not using this file, you can use this if needed, for now fub.js is used, Read the comments in that file for Why!

export const typeDef = `#graphql
  scalar GraphQLJSON

  type Deals {
  pipelineId: Int
  stageId: Int
  enteredStageAt: String
  id: Int
  name: String
  type: Int
  status: String
  price: Int
  createdAt: String
  orderWeight: Int
  description: String
  projectedCloseDate: String
  customField1: String
  agentCommission: Int
  teamCommission: Int
  users: [Users]
  people: [People]
  _metadata: Metadata
  _additionalProperties: GraphQLJSON
}

type Teams {
  id: Int
  name: String
  leaderIds: [Int]
  userIds: [Int]
}

type Metadata {
  collection: String
  offset: Int
  limit: Int
  total: Int
  next: String
  nextLink: String
  totalByStageId: GraphQLJSON # Only for Deals API
}

type Ponds {
  id: Int
  name: String
  userId: Int
  userIds: [Int]
}

type Groups {
  id: Int
  name: String
  type: String
  distribution: String
  defaultUserId: String
  defaultPondId: String
  defaultGroupId: String
  claimWindow: Int
  nextRoundRobinUser: String
  isPrimary: Boolean
  users: [Users]
}

type Textmessage {
  id: Int
  created: String
  updated: String
  createdById: Int
  updatedById: Int
  personId: Int
  name: String
  firstName: String
  lastName: String
  picture: String
  userId: Int
  userName: String
  status: String
  message: String
  fromNumber: String
  toNumber: String
  sent: String
  isIncoming: Boolean
  archived: Boolean
  read: Boolean
  sharedInboxId: Int
  actionPlanId: Int
  groupTextId: String
  isExternal: Boolean
  externalUrl: String
  externalLabel: String
  systemName: String
  media: [String]
}

type TextMessages {
  textmessages: [Textmessage]
  _metadata: Metadata
}

type DealCustomfields {
  id: Int
  label: String
  name: String
  type: String
  orderWeight: Int
  hideIfEmpty: Boolean
  readOnly: Boolean
}

type Pipelines {
  id: Int
  name: String
  description: String
  orderWeight: Int
  stages: [Stages]
}

type WebhookEvents {
  id: String
  eventCreated: String
  event: String
  uri: String
  resourceIds: [Int]
}

type Webhooks {
  id: Int
  event: String
  status: String
  url: String
}

type Appointmentoutcomes {
  id: Int
  name: String
  orderWeight: Int
}

type AppointmentOutcomes {
  appointmentoutcomes: [Appointmentoutcomes]
  _metadata: Metadata
}

type Appointmenttypes {
  id: Int
  name: String
  orderWeight: Int
}

type AppointmentTypes {
  appointmenttypes: [Appointmenttypes]
  _metadata: Metadata
}

type Invitees {
  userId: Int
  personId: String
  name: String
  email: String
  picture: String
}

type Appointments {
  id: Int
  created: String
  updated: String
  createdById: Int
  updatedById: Int
  title: String
  description: String
  start: String
  end: String
  allDay: Boolean
  originFub: Boolean
  location: String
  typeId: String
  type: String
  outcomeId: String
  outcome: String
  externalEventLink: String
  externalCalendarId: String
  isEditable: Boolean
  detailsVisible: Boolean
  invitees: [Invitees]
}

type Tasks {
  id: Int
  created: String
  updated: String
  completed: String
  createdBy: String
  updatedBy: String
  personId: Int
  AssignedTo: String
  assignedUserId: Int
  name: String
  type: String
  isCompleted: Int
  dueDate: String
  dueDateTime: String
  externalTaskLink: String
  externalCalendarId: String
  remindSecondsBefore: String
}

type Stages {
  id: Int
  name: String
  orderWeight: Int
  isProtected: Boolean
  peopleCount: Int
}

type Customfields {
  id: Int
  label: String
  name: String
  type: String
  isRecurring: Boolean
}

type EmEvents {
  count: Int
  type: String
  personId: Int
  campaignId: Int
  campaignName: String
  created: String
  updated: String
}

type EmailmarketingEvents {
  emEvents: [EmEvents]
  _metadata: Metadata
}

type Textmessagetemplates {
  id: Int
  name: String
  totalSent: Int
  totalReplies: Int
  message: String
  isShared: Boolean
  createdBy: Int
  isEditable: Boolean
  isDeletable: Boolean
  isShareable: Boolean
  actionPlans: [String]
  sentPeopleIds: [Int]
}

type Texttemplates {
  textmessagetemplates: [Textmessagetemplates]
  _metadata: Metadata
}

type Templates {
  id: Int
  created: String
  updated: String
  createdById: Int
  updatedById: Int
  name: String
  isMobile: Int
  isShared: Boolean
  body: String
  subject: String
  isEditable: Boolean
  isDeletable: Boolean
  actionPlans: [ActionPlans]
}

type Emailtemplates {
  templates: [Templates]
  _metadata: Metadata
}

type ActionPlans {
  id: Int
  created: String
  updated: String
  name: String
  status: String
}

type Actionplans {
  actionPlans: [ActionPlans]
  _metadata: Metadata
}

type Smartlists {
  id: Int
  name: String
  isFub2: Boolean
  description: String
  defaultSmartListId: String
}

type Users {
  id: Int
  created: String
  updated: String
  name: String
  firstName: String
  lastName: String
  email: String
  phone: String
  role: String
  status: String
  timezone: String
  beta: Boolean
  pauseLeadDistribution: Boolean
  lastSeenIos: String
  lastSeenAndroid: String
  lastSeenFub2: String
  canExport: Boolean
  canCreateApiKeys: Boolean
  isOwner: Boolean
  leadEmailAddress: String
  teamLeaderOf: [String]
  teamIds: [Int]
  groups: [Groups]
  picture: [String]
}

type Calls {
  id: Int
  created: String
  updated: String
  createdById: Int
  updatedById: Int
  phone: String
  personId: Int
  userId: Int
  userName: String
  note: String
  outcome: String
  isIncoming: Boolean
  duration: Int
  ringDuration: Int
}

type Notes {
  id: Int
  created: String
  updated: String
  createdBy: String
  updatedBy: String
  personId: Int
  subject: String
  body: String
  type: String
  isHtml: Int
}

type User {
  id: Int
  name: String
  email: String
}

type Owner {
  name: String
  email: String
}

type Account {
  id: Int
  domain: String
  owner: Owner
}

type Identity {
  user: User
  account: Account
}

type Phones {
  value: String
  type: String
  status: String
  isPrimary: Int
  normalized: String
}

type Peoplerelationships {
  id: Int
  created: String
  updated: String
  createdById: Int
  updatedById: Int
  personId: Int
  name: String
  firstName: String
  lastName: String
  type: String
  isPriority: Boolean
  picture: String
  socialData: [String]
  addresses: [String]
  phones: [Phones]
  emails: [String]
}

type Picture {
  small: String
}

type Addresses {
  type: String
  street: String
  city: String
  state: String
  code: String
  country: String
}

type Emails {
  value: String
  type: String
  isPrimary: Int
  status: String
}

type Collaborators {
  id: Int
  name: String
  assigned: Boolean
  role: String
}

type People {
  id: Int
  created: String
  updated: String
  createdVia: String
  lastActivity: String
  name: String
  firstName: String
  lastName: String
  stage: String
  source: String
  sourceUrl: String
  contacted: Int
  price: Int
  assignedLenderId: String
  assignedLenderName: String
  assignedUserId: Int
  assignedTo: String
  picture: Picture
  addresses: [Addresses]
  phones: [Phones]
  emails: [Emails]
  tags: [String]
  collaborators: [Collaborators]
  _additionalProperties: GraphQLJSON
}

type Person {
  people: [People]
  _metadata: Metadata
}

type Property {
  street: String
  city: String
  state: String
  code: String
  mlsNumber: String
  price: String
  forRent: String
  url: String
  type: String
  bedrooms: String
  bathrooms: String
  area: String
  lot: String
}

type Events {
  id: Int
  created: String
  updated: String
  personId: Int
  message: String
  description: String
  noteId: Int
  source: String
  type: String
  pageTitle: String
  pageUrl: String
  pageDuration: Int
  property: Property
}

type Query {
  Deals: Deals
  Teams: Teams
  Ponds: Ponds
  Groups: Groups
  TextMessages: TextMessages
  DealCustomfields: DealCustomfields
  Pipelines: Pipelines
  WebhookEvents: WebhookEvents
  Webhooks: Webhooks
  AppointmentOutcomes: AppointmentOutcomes
  AppointmentTypes: AppointmentTypes
  Appointments: Appointments
  tasks: Tasks
  stages: Stages
  customfields: Customfields
  emailmarketingEvents: EmailmarketingEvents
  texttemplates: Texttemplates
  emailtemplates: Emailtemplates
  actionplans: Actionplans
  smartlists: Smartlists
  users: Users
  calls: Calls
  notes: Notes
  identity: Identity
  peoplerelationships: [Peoplerelationships]
  person: Person
  events: Events
}

# Types with identical fields:
# Appointmentoutcomes Appointmenttypes
`;