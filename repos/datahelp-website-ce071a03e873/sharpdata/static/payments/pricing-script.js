$(document).ready(function () {

    const fubSisuAddonPricing = {
        addon_assignment: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        addon_custom_branded_theme: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        addon_custom_thank_you_message: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        addon_appointment_template: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: 5, setup_fee: "N/A" },
        },
        addon_bi_directional_sync: {
            dropdown: false,
            fea: { price: 20, setup_fee: 49 },
            wpp: { price: 20, setup_fee: 49 },
            wpm: { price: 15, setup_fee: 49 },
        },
        addon_document_upload_for_forms: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        addon_additional_custom_fields_that_sync_with_sisu: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: 49 },
            wpm: { price: 10, setup_fee: 49 },
        },
        addon_additional_option_fields: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 15, setup_fee: 19 },
            wpm: { price: 10, setup_fee: 19 },
        },
        addon_additional_optional_automation: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: 99 },
            wpm: { price: 15, setup_fee: 99 },
        },
    };

    const fubOtcAddonPricing = {
        fubotc_addon_assignment: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        fubotc_addon_custom_branded_theme: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        fubotc_addon_custom_thank_you_message: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        fubotc_addon_appointment_template: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: 5, setup_fee: "N/A" },
        },
        fubotc_addon_bi_directional_sync: {
            dropdown: false,
            fea: { price: 20, setup_fee: 49 },
            wpp: { price: 20, setup_fee: 49 },
            wpm: { price: 15, setup_fee: 49 },
        },
        fubotc_addon_document_upload_for_forms: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        fubotc_addon_additional_custom_fields_that_sync_with_otc: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: 49 },
            wpm: { price: 10, setup_fee: 49 },
        },
        fubotc_addon_additional_option_fields: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 15, setup_fee: 19 },
            wpm: { price: 10, setup_fee: 19 },
        },
        fubotc_addon_additional_optional_automation: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: 99 },
            wpm: { price: 15, setup_fee: 99 },
        },
    };

    const fubSisuOtcAddonPricing = {
        fubsisuotc_addon_assignment: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        fubsisuotc_addon_custom_branded_theme: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        fubsisuotc_addon_custom_thank_you_message: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        fubsisuotc_addon_appointment_template: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: 5, setup_fee: "N/A" },
        },
        fubsisuotc_addon_bi_directional_sync: {
            dropdown: false,
            fea: { price: 20, setup_fee: 49 },
            wpp: { price: 20, setup_fee: 49 },
            wpm: { price: 15, setup_fee: 49 },
        },
        fubsisuotc_addon_document_upload_for_forms: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        fubsisuotc_addon_additional_custom_fields_that_sync_with_sisu: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: 49 },
            wpm: { price: 10, setup_fee: 49 },
        },
        fubsisuotc_addon_additional_custom_fields_that_sync_with_otc: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: 49 },
            wpm: { price: 10, setup_fee: 49 },
        },
        fubsisuotc_addon_additional_option_fields: {
            dropdown: true,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 15, setup_fee: 19 },
            wpm: { price: 10, setup_fee: 19 },
        },
        fubsisuotc_addon_additional_optional_automation: {
            dropdown: false,
            fea: { price: "N/A", setup_fee: "N/A" },
            wpp: { price: 20, setup_fee: 99 },
            wpm: { price: 15, setup_fee: 99 },
        },
    };

    const otcOnlyAddonPricing = {
        otconly_addon_custom_branded_theme: {
            dropdown: false,
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        otconly_addon_custom_thank_you_message: {
            dropdown: false,
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        otconly_addon_appointment_template: {
            dropdown: true,
            wpp: { price: 10, setup_fee: "N/A" },
            wpm: { price: 5, setup_fee: "N/A" },
        },
        otconly_addon_bi_directional_sync: {
            dropdown: false,
            wpp: { price: 20, setup_fee: 49 },
            wpm: { price: 15, setup_fee: 49 },
        },
        otconly_addon_document_upload_for_forms: {
            dropdown: false,
            wpp: { price: 20, setup_fee: "N/A" },
            wpm: { price: "N/A", setup_fee: "N/A" },
        },
        otconly_addon_additional_custom_fields_that_sync_with_sisu: {
            dropdown: true,
            wpp: { price: 20, setup_fee: 49 },
            wpm: { price: 10, setup_fee: 49 },
        },
        otconly_addon_additional_option_fields: {
            dropdown: true,
            wpp: { price: 15, setup_fee: 19 },
            wpm: { price: 10, setup_fee: 19 },
        },
        otconly_addon_additional_optional_automation: {
            dropdown: false,
            wpp: { price: 20, setup_fee: 99 },
            wpm: { price: 15, setup_fee: 99 },
        },
    };

    $('#collapseTwo').on('change', function () {
        var orignal_fea_price = 59;
        var orignal_wpp_price = 199;
        var orignal_wpm_price = 299;
        for (item in fubSisuAddonPricing) {
            if ($('#collapseTwo #' + item).prop("checked")) {
                var addon_price = 0;
                var addon_setup_fee = 0;
                var addon_drop_down = 1;
                if (fubSisuAddonPricing[item].dropdown != false) {
                    addon_drop_down = $("#collapseTwo #" + item + "_select option:selected").val();
                    console.log(addon_drop_down);
                }
                /*FUB Embeded App Price Update */
                if (fubSisuAddonPricing[item].fea.price != 'N/A') {
                    addon_price = fubSisuAddonPricing[item].fea.price * addon_drop_down;
                }
                if (fubSisuAddonPricing[item].fea.setup_fee != 'N/A') {
                    addon_setup_fee = fubSisuAddonPricing[item].fea.setup_fee;
                }
                orignal_fea_price = orignal_fea_price + addon_price + addon_setup_fee;

                /*Webform Pipeline Plus Price Update */
                if (fubSisuAddonPricing[item].wpp.price != 'N/A') {
                    addon_price = fubSisuAddonPricing[item].wpp.price * addon_drop_down;
                }
                if (fubSisuAddonPricing[item].wpp.setup_fee != 'N/A') {
                    addon_setup_fee = fubSisuAddonPricing[item].wpp.setup_fee;
                }
                orignal_wpp_price = orignal_wpp_price + addon_price + addon_setup_fee;

                /*Webform Pipeline Plus Price Update */
                if (fubSisuAddonPricing[item].wpm.price != 'N/A') {
                    addon_price = fubSisuAddonPricing[item].wpm.price * addon_drop_down;
                }
                if (fubSisuAddonPricing[item].wpm.setup_fee != 'N/A') {
                    addon_setup_fee = fubSisuAddonPricing[item].wpm.setup_fee;
                }
                orignal_wpm_price = orignal_wpm_price + addon_price + addon_setup_fee;
            }
        }

        $('#fea span').text(orignal_fea_price);
        $('#wpp span').text(orignal_wpp_price);
        $('#wpm span').text(orignal_wpm_price);
    });

    /** FUB-OTC */
    $('#collapseThree').on('change', function () {
        var orignal_fea_price = 59;
        var orignal_wpp_price = 199;
        var orignal_wpm_price = 299;
        for (item in fubOtcAddonPricing) {
            if ($('#collapseThree #' + item).prop("checked")) {
                var addon_price = 0;
                var addon_setup_fee = 0;
                var addon_drop_down = 1;
                if (fubOtcAddonPricing[item].dropdown != false) {
                    addon_drop_down = $("#collapseThree #" + item + "_select option:selected").val();
                }
                /*FUB Embeded App Price Update */
                if (fubOtcAddonPricing[item].fea.price != 'N/A') {
                    addon_price = fubOtcAddonPricing[item].fea.price * addon_drop_down;
                }
                if (fubOtcAddonPricing[item].fea.setup_fee != 'N/A') {
                    addon_setup_fee = fubOtcAddonPricing[item].fea.setup_fee;
                }
                orignal_fea_price = orignal_fea_price + addon_price + addon_setup_fee;

                /*Webform Pipeline Plus Price Update */
                if (fubOtcAddonPricing[item].wpp.price != 'N/A') {
                    addon_price = fubOtcAddonPricing[item].wpp.price * addon_drop_down;
                }
                if (fubOtcAddonPricing[item].wpp.setup_fee != 'N/A') {
                    addon_setup_fee = fubOtcAddonPricing[item].wpp.setup_fee;
                }
                orignal_wpp_price = orignal_wpp_price + addon_price + addon_setup_fee;

                /*Webform Pipeline Plus Price Update */
                if (fubOtcAddonPricing[item].wpm.price != 'N/A') {
                    addon_price = fubOtcAddonPricing[item].wpm.price * addon_drop_down;
                }
                if (fubOtcAddonPricing[item].wpm.setup_fee != 'N/A') {
                    addon_setup_fee = fubOtcAddonPricing[item].wpm.setup_fee;
                }
                orignal_wpm_price = orignal_wpm_price + addon_price + addon_setup_fee;
            }
        }

        $('#collapseThree #fea span').text(orignal_fea_price);
        $('#collapseThree #wpp span').text(orignal_wpp_price);
        $('#collapseThree #wpm span').text(orignal_wpm_price);
    });


    /**FUB-SISU-OTC */
    $('#collapseFive').on('change', function () {
        var orignal_fea_price = 59;
        var orignal_wpp_price = 199;
        var orignal_wpm_price = 299;
        for (item in fubSisuOtcAddonPricing) {
            if ($('#collapseFive #' + item).prop("checked")) {
                
                var addon_price = 0;
                var addon_setup_fee = 0;
                var addon_drop_down = 1;
                if (fubSisuOtcAddonPricing[item].dropdown != false) {
                    addon_drop_down = $("#collapseFive #" + item + "_select option:selected").val();
                    
                }
                /*FUB Embeded App Price Update */
                if (fubSisuOtcAddonPricing[item].fea.price != 'N/A') {
                    addon_price = fubSisuOtcAddonPricing[item].fea.price * addon_drop_down;
                }
                if (fubSisuOtcAddonPricing[item].fea.setup_fee != 'N/A') {
                    addon_setup_fee = fubSisuOtcAddonPricing[item].fea.setup_fee;
                }
                orignal_fea_price = orignal_fea_price + addon_price + addon_setup_fee;
                /*Webform Pipeline Plus Price Update */
                if (fubSisuOtcAddonPricing[item].wpp.price != 'N/A') {
                    addon_price = fubSisuOtcAddonPricing[item].wpp.price * addon_drop_down;
                }
                if (fubSisuOtcAddonPricing[item].wpp.setup_fee != 'N/A') {
                    addon_setup_fee = fubSisuOtcAddonPricing[item].wpp.setup_fee;
                }
                orignal_wpp_price = orignal_wpp_price + addon_price + addon_setup_fee;

                /*Webform Pipeline Plus Price Update */
                if (fubSisuOtcAddonPricing[item].wpm.price != 'N/A') {
                    addon_price = fubSisuOtcAddonPricing[item].wpm.price * addon_drop_down;
                }
                if (fubSisuOtcAddonPricing[item].wpm.setup_fee != 'N/A') {
                    addon_setup_fee = fubSisuOtcAddonPricing[item].wpm.setup_fee;
                }
                orignal_wpm_price = orignal_wpm_price + addon_price + addon_setup_fee;
            }
        }

        $('#collapseFive #fea span').text(orignal_fea_price);
        $('#collapseFive #wpp span').text(orignal_wpp_price);
        $('#collapseFive #wpm span').text(orignal_wpm_price);
    });

    /**OTC-Only */
    $('#collapseFour').on('change', function () {
        var orignal_fea_price = 59;
        var orignal_wpp_price = 199;
        var orignal_wpm_price = 299;
        for (item in otcOnlyAddonPricing) {
            if ($('#collapseFour #' + item).prop("checked")) {
                
                var addon_price = 0;
                var addon_setup_fee = 0;
                var addon_drop_down = 1;
                if (otcOnlyAddonPricing[item].dropdown != false) {
                    addon_drop_down = $("#collapseFour #" + item + "_select option:selected").val();
                    
                }
                /*Webform Pipeline Plus Price Update */
                if (otcOnlyAddonPricing[item].wpp.price != 'N/A') {
                    addon_price = otcOnlyAddonPricing[item].wpp.price * addon_drop_down;
                }
                if (otcOnlyAddonPricing[item].wpp.setup_fee != 'N/A') {
                    addon_setup_fee = otcOnlyAddonPricing[item].wpp.setup_fee;
                }
                orignal_wpp_price = orignal_wpp_price + addon_price + addon_setup_fee;

                /*Webform Pipeline Plus Price Update */
                if (otcOnlyAddonPricing[item].wpm.price != 'N/A') {
                    addon_price = otcOnlyAddonPricing[item].wpm.price * addon_drop_down;
                }
                if (otcOnlyAddonPricing[item].wpm.setup_fee != 'N/A') {
                    addon_setup_fee = otcOnlyAddonPricing[item].wpm.setup_fee;
                }
                orignal_wpm_price = orignal_wpm_price + addon_price + addon_setup_fee;
            }
        }

        $('#collapseFour #wpp span').text(orignal_wpp_price);
        $('#collapseFour #wpm span').text(orignal_wpm_price);
    });

    $('.custom-switch input').on("click" , function(){
        if($(this).prop("checked")){
            $('.custom-switch input').each(function(){
                    $(this).prop("checked", true);
            });
            $('.tableprow td p').each(function(){
                $(this).addClass("annual-strike");
            });
        }
        else{
            $('.custom-switch input').each(function(){
                $(this).prop("checked", false);
            });
            $('.tableprow td p').each(function(){
                $(this).removeClass("annual-strike");
            });
        }
    });
});