export var templates = [
    {
        'template_id': 'FubCallByAssignedAgentToCustomField',
        'template_name': 'Last Call By Assigned Agent',
        'template_description': 'Updates Custom Field with date of last call by assigned agent',
        'status': false,
    },
    {
        'template_id': 'FubEmailByAssignedAgentToCustomField',
        'template_name': 'Last Email By Assigned Agent',
        'template_description': 'Updates Custom Field with date of last Email by assigned agent',
        'status': false,
    },
    {
        'template_id': 'FubTextByAssignedAgentToCustomField',
        'template_name': 'Last Text By Assigned Agent',
        'template_description': 'Updates Custom Field with date of last Text by assigned agent',
        'status': false,
    },
]

export var template_workflows = {
    'FubCallByAssignedAgentToCustomField': [
           {
            // a lot of details in here come from frontend, hence have to keep it here, eventually the plan is to not ue it.
            "action_id": "trigger",
            "api_name": "trigger",
            "api_type": "trigger",
            "data_mapper": {
                // We use this to show in frontend, not a great idea, I know :(
            "name": "Calls Created",
            "description": "Triggered when a call is Created",
             "platform": "FUB",
             "type": "callsCreated"
            },
            "is_default": false,
            "next_action_ids": [
                "AdvanceFilter653204721"
               ],
            "test_status": "SUCCESS"
           },
           {
            "action_id": "AdvanceFilter653204721",
            "api_name": "",
            "api_type": "",
            "data_mapper": {
             "conditions":
             [[
                {
                 "!#data_type": "bool",
                 "!#expected_value": false,
                 "!#operator": "equals",
                 "!#value": "{{trigger__call__isIncoming}}"
                },
                {
                 "!#data_type": "number",
                 "!#expected_value": "",
                 "!#operator": "exists",
                 "!#value": "{{trigger__call__systemId}}"
                },
                {
                 "!#data_type": "text",
                 "!#expected_value": "{{trigger__call__userId}}",
                 "!#operator": "equals",
                 "!#value": "{{trigger__person__assignedUserId}}"
                }
               ]]
            },
            "is_default": false,
            "meta_data": {
             "automation_name": "",
             "filterType": "advance"
            },
            "next_action_ids": [
             "FUB9815612364"
            ],
            "platform": "FILTER",
            "test_status": "SUCCESS"
           },
           {
            "action_id": "FUB9815612364",
            "api_name": "",
            "api_type": "",
            "automation_name": "Populate Custom Fields",
            "data_mapper": {
             "customfields": [
              {
               "key": "customLastCallByAssignedAgent",
               "value": "{{todays_date}}"
              },
            //   {
            //     "key": "customLastCommunicationByAssignedAgent",
            //     "value": "{{todays_date}}"
            //    }
             ]
            },
            "is_default": false,
            "next_action_ids": [
            ],
            "platform": "FUB",
            "test_status": "SUCCESS"
           }
    ],
    'FubEmailByAssignedAgentToCustomField': [
        {
         // a lot of details in here come from frontend, hence have to keep it here, eventually the plan is to not ue it.
         "action_id": "trigger",
         "api_name": "trigger",
         "api_type": "trigger",
         "data_mapper": {
             // We use this to show in frontend, not a great idea, I know :(
         "name": "Emails Created",
         "description": "Triggered when an email is created",
          "platform": "FUB",
          "type": "emailsCreated"
         },
         "is_default": false,
         "next_action_ids": [
             "AdvanceFilter653204721"
            ],
         "test_status": "SUCCESS"
        },
        {
         "action_id": "AdvanceFilter653204721",
         "api_name": "",
         "api_type": "",
         "data_mapper": {
          "conditions":
          [
            [
                {
                 "!#data_type": "text",
                 "!#expected_value": "{{trigger__email__userId}}",
                 "!#operator": "equals",
                 "!#value": "{{trigger__person__assignedUserId}}"
                },
                {
                 "!#data_type": "text",
                 "!#expected_value": "sent,queued",
                 "!#operator": "in",
                 "!#value": "{{trigger__email__status}}"
                }
               ]
        ]
         },
         "is_default": false,
         "meta_data": {
          "automation_name": "",
          "filterType": "advance"
         },
         "next_action_ids": [
          "FUB9815612364"
         ],
         "platform": "FILTER",
         "test_status": "SUCCESS"
        },
        {
         "action_id": "FUB9815612364",
         "api_name": "",
         "api_type": "",
         "automation_name": "Populate Custom Fields",
         "data_mapper": {
          "customfields": [
           {
            "key": "customLastEmailByAssignedAgent",
            "value": "{{todays_date}}"
           },
         //   {
         //     "key": "customLastCommunicationByAssignedAgent",
         //     "value": "{{todays_date}}"
         //    }
          ]
         },
         "is_default": false,
         "next_action_ids": [
         ],
         "platform": "FUB",
         "test_status": "SUCCESS"
        }
 ],
 'FubTextByAssignedAgentToCustomField': [
    {
     // a lot of details in here come from frontend, hence have to keep it here, eventually the plan is to not ue it.
     "action_id": "trigger",
     "api_name": "trigger",
     "api_type": "trigger",
     "data_mapper": {
         // We use this to show in frontend, not a great idea, I know :(
     "name": "TextMessage Created",
     "description": "Triggered when a text message is Sent or Received",
      "platform": "FUB",
      "type": "textMessagesCreated"
     },
     "is_default": false,
     "next_action_ids": [
         "AdvanceFilter653204721"
        ],
     "test_status": "SUCCESS"
    },
    {
     "action_id": "AdvanceFilter653204721",
     "api_name": "",
     "api_type": "",
     "data_mapper": {
      "conditions":
      [
        [
            {
             "!#data_type": "bool",
             "!#expected_value": false,
             "!#operator": "equals",
             "!#value": "{{trigger__text__isIncoming}}"
            },
            {
             "!#data_type": "bool",
             "!#expected_value": false,
             "!#operator": "equals",
             "!#value": "{{trigger__text__isExternal}}"
            },
            {
             "!#data_type": "text",
             "!#expected_value": "{{trigger__text__userId}}",
             "!#operator": "equals",
             "!#value": "{{trigger__person__assignedUserId}}"
            }
           ]
    ]
     },
     "is_default": false,
     "meta_data": {
      "automation_name": "",
      "filterType": "advance"
     },
     "next_action_ids": [
      "FUB9815612364"
     ],
     "platform": "FILTER",
     "test_status": "SUCCESS"
    },
    {
     "action_id": "FUB9815612364",
     "api_name": "",
     "api_type": "",
     "automation_name": "Populate Custom Fields",
     "data_mapper": {
      "customfields": [
       {
        "key": "customLastTextByAssignedAgent",
        "value": "{{todays_date}}"
       },
     //   {
     //     "key": "customLastCommunicationByAssignedAgent",
     //     "value": "{{todays_date}}"
     //    }
      ]
     },
     "is_default": false,
     "next_action_ids": [
     ],
     "platform": "FUB",
     "test_status": "SUCCESS"
    }
]
}