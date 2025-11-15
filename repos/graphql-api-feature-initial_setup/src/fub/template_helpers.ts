import { FubAPI } from "./helper.js";

const create_custom_field = async (cutomfieldlabel: string, customfieldtype: string, fub_key: string) => {
    const fub = new FubAPI(fub_key);
    // get custom fields
    const resp = await fub.get_all_data("customfields");
    const status = resp.status;
    const custom_fields: any = await resp.json();
    if (status >= 300) {
        return {"data": custom_fields, "statusCode": status};
    }
    console.log("custom_fields", custom_fields)
    
    // check if custom field exsists
    const custom_field = custom_fields.find((custom_field: any) => {
        return custom_field["label"] == cutomfieldlabel && custom_field["type"] == customfieldtype;
    })
    console.log("custom_field found", custom_field)
    // if custom field doesn't exsist create it
    if (!custom_field) {
        const data = {
            "label": cutomfieldlabel,
            // "name": "customLastCallByAssignedAgent",
            "type": customfieldtype,
        }
        const resp = await fub.post("customfields", data)
        const status = resp.status;
        var custom_field_info: any = await resp.json();
        if (status >= 300) {
            return {"data": custom_field_info, "statusCode": status};
        }
    }
    return {"data": custom_field_info, "statusCode": 200};
}
export const setup_fub_for_template = async (template_id: string, fub_key: string) => {
    console.log("setup_fub_for_template", template_id, fub_key)
    if  (template_id == "FubCallByAssignedAgentToCustomField") {
    const lastcallcutomfieldlabel = 'Last Call By Assigned Agent'
    const customfieldtype = 'date'
    // const lastcommcustomfieldlabel = 'Last Communication By Assigned Agent'
    let data = await create_custom_field(lastcallcutomfieldlabel, customfieldtype, fub_key);
    if (data["statusCode"] >= 300) {
        return data;
    }
    // let _data = create_custom_field(lastcommcustomfieldlabel, customfieldtype, fub_key);
    // if (_data["statusCode"] >= 300) {
    //     return _data;
    // }
    return {"data": {}, "statusCode": 200};
}
else if (template_id == "FubEmailByAssignedAgentToCustomField") {
    const lastcallcutomfieldlabel = 'Last Email By Assigned Agent'
    const customfieldtype = 'date'
    // const lastcommcustomfieldlabel = 'Last Communication By Assigned Agent'
    let data = await create_custom_field(lastcallcutomfieldlabel, customfieldtype, fub_key);
    if (data["statusCode"] >= 300) {
        return data;
    }
    // let _data = create_custom_field(lastcommcustomfieldlabel, customfieldtype, fub_key);
    // if (_data["statusCode"] >= 300) {
    //     return _data;
    // }
    return {"data": {}, "statusCode": 200};
}
else if (template_id == "FubTextByAssignedAgentToCustomField") {
    const lastcallcutomfieldlabel = 'Last Text By Assigned Agent'
    const customfieldtype = 'date'
    // const lastcommcustomfieldlabel = 'Last Communication By Assigned Agent'
    let data = await create_custom_field(lastcallcutomfieldlabel, customfieldtype, fub_key);
    if (data["statusCode"] >= 300) {
        return data;
    }
    // let _data = create_custom_field(lastcommcustomfieldlabel, customfieldtype, fub_key);
    // if (_data["statusCode"] >= 300) {
    //     return _data;
    // }
    return {"data": {}, "statusCode": 200};
}

}
