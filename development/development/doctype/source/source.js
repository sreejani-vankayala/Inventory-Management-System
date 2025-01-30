// Copyright (c) 2025, sreejani and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Source", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Source', {
    after_save: function (frm) {
        if (frm.doc.full_name) {
            frappe.call({
                method: "development.development.doctype.source.source.update_destination",
                args: {
                    full_name: frm.doc.full_name
                },
                callback: function (response) {
                    if (response.message) {
                        if (response.message.status === "success") {
                            frappe.msgprint({
                                title: __('Success'),
                                message: response.message.message,
                                indicator: 'green'
                            });
                        } else if (response.message.status === "exists") {
                            frappe.msgprint({
                                title: __('Info'),
                                message: response.message.message,
                                indicator: 'blue'
                            });
                        }
                    }
                }
            });
        } else {
            frappe.msgprint({
                title: __('Validation Error'),
                message: __('Full Name is required to update the Destination doctype.'),
                indicator: 'red'
            });
        }
    }
});

