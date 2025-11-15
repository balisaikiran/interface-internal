export const triggers = {
    "People": {
        "peopleCreated": {
            "name": "Person Created",
            "description": "Triggered when a person is created",
        },
        "peopleUpdated": {
            "name": "Person Updated",
            "description": "Triggered when a person is updated",
        },
        "peopleDeleted": {
            "name": "Person Deleted",
            "description": "Triggered when a person is deleted",
        },
        "peopleTagsCreated": {
            "name": "Tags Created",


            "description": "Triggered when a Tag is added to a person",
        },
        "peopleStageUpdated": {
            "name": "Person Stage Updated",
            "description": "Triggered when a person stage is updated",
        },
        // "peopleRelationshipCreated": {
        //     "name": "Person Relationship Created",
        //     "description": "Triggered when a person relationship is created",
        // },
        // "peopleRelationshipUpdated": {
        //     "name": "Person Relationship Updated",
        //     "description": "Triggered when a person relationship is updated",
        // },
        // "peopleRelationshipDeleted": {
        //     "name": "Person Relationship Deleted",
        //     "description": "Triggered when a person relationship is deleted",
        // },
    },
    "notes": {
        "notesCreated": {
            "name": "Note Created",
            "description": "Triggered when a note is created",
        },
        "notesUpdated": {
            "name": "Note Updated",
            "description": "Triggered when a note is updated",
        }
    },
    // "notesDeleted": {
    //     "name": "Note Deleted",
    //     "description": "Triggered when a note is deleted",
    // },
    "emails": {
        "emailsCreated": {
            "name": "Email Created",
            "description": "Triggered when an email is created",
        },
        "emailsUpdated": {
            "name": "Email Updated",
            "description": "Triggered when an email is updated",
        },
        // "emailsDeleted": {
        //     "name": "Email Deleted",
        //     "description": "Triggered when an email is deleted",
        // },
    },
    // "tasks": {
    //     "tasksCreated": {
    //         "name": "Task Created",
    //         "description": "Triggered when a task is created",
    //     },
    //     "tasksUpdated": {
    //         "name": "Task Updated",
    //         "description": "Triggered when a task is updated",
    //     },
    //     "tasksDeleted": {
    //         "name": "Task Deleted",
    //         "description": "Triggered when a task is deleted",
    //     },
    // },
    "appointments": {
        "appointmentsCreated": {
            "name": "Appointment Created",
            "description": "Triggered when an appointment is created",
        },
        "appointmentsUpdated": {
            "name": "Appointment Updated",
            "description": "Triggered when an appointment is updated",
        },
        // "appointmentsDeleted": {
        //     "name": "Appointment Deleted",
        //     "description": "Triggered when an appointment is deleted",
        // },
    },
    "textMessages": {
        "textMessagesCreated": {
            "name": "TextMessage Created",
            "description": "Triggered when a text message is Sent or Received",
        },
        // "textMessagesUpdated": {
        //     "name": "TextMessage Updated",
        //     "description": "Triggered when a text message is updated",
        // },
        // "textMessagesDeleted": {
        //     "name": "TextMessage Deleted",
        //     "description": "Triggered when a text message is deleted",
        // },
    },
    "calls": {
        "callsCreated": {
            "name": "Calls Created",
            "description": "Triggered when a call is created",
        },
        "callsUpdated": {
            "name": "Calls Updated",
            "description": "Triggered when a call is updated",
        },
        // "callsDeleted": {
        //     "name": "Calls Deleted",
        //     "description": "Triggered when a call is deleted",
        // },
    },
    // "Marketing Emails": {
    //     "emEventsOpened": {
    //         "name": "Email Opened",
    //         "description": "Triggered when an email is opened",
    //     },
    //     "emEventsClicked": {
    //         "name": "Email Clicked",
    //         "description": "Triggered when an email is clicked",
    //     },
    //     "emEventsUnsubscribed": {
    //         "name": "Email Unsubscribed",
    //         "description": "Triggered when an email is unsubscribed",
    //     },
    // },
    "deals": {
        "dealsCreated": {
            "name": "Deal Created",
            "description": "Triggered when a deal is created",
        },
        "dealsUpdated": {
            "name": "Deal Updated",
            "description": "Triggered when a deal is updated",
        },
        "dealsDeleted": {
            "name": "Deal Deleted",
            "description": "Triggered when a deal is deleted",
        },
    },
    // "Events": {
    //     "eventsCreated": {
    //         "name": "Event Created",
    //         "description": "Triggered when People perform an action on your IDX website, e.g. view a property.",
    //     },
    // }
}
// All triggers types, make it flattened list
export const triggers_types = Object.values(triggers).map((trigger) => Object.keys(trigger)).flat();
console .log("triggers_types", triggers_types);
