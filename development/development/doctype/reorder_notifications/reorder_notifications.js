// Copyright (c) 2025, sreejani and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Reorder Notifications", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Reorder Notifications', {
    refresh: function(frm) {
        frm.add_custom_button('Send Reorder Notifications', function() {
            function check_and_send_reorder_notifications() {
                if (!frm.doc.item_code || !frm.doc.reorder_level || !frm.doc.notification_recipient) {
                    frappe.msgprint('Please ensure Item Code, Reorder Level, and Notification Recipient fields are filled.');
                    return;
                }

                if (frm.doc.reorder_level < 30) {
                    frappe.call({
                        method: "development.development.doctype.reorder_notifications.reorder_notifications.send_reorder_notification_email",
                        args: {
                            recipient: frm.doc.notification_recipient,
                            item_name: frm.doc.item_code,
                            reorder_level: frm.doc.reorder_level
                        },
                        callback: function(response) {
                            if (response.message) {
                                frappe.msgprint(`Email sent to ${frm.doc.notification_recipient}`);
                                frm.set_value('email_sent', 1); 
                            } else {
                                frappe.msgprint(`Failed to send email to ${frm.doc.notification_recipient}`);
                            }
                        },
                        error: function(error) {
                            frappe.msgprint(`Error sending email to ${frm.doc.notification_recipient}`);
                        }
                    });
                } else {
                    frappe.msgprint('Reorder level is not below 20. No email will be sent.');
                }
            }

            check_and_send_reorder_notifications();
        });
    }
});
