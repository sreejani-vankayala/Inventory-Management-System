# Copyright (c) 2025, sreejani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ReorderNotifications(Document):
	pass


@frappe.whitelist()
def send_reorder_notification_email(recipient, item_name, reorder_level):
    subject = "Reorder Notification"
    message = f"""
        Dear User,<br><br>
        The stock level for the item <b>{item_name}</b> has fallen below the reorder level of <b>{reorder_level}</b>.<br><br>
        Please take necessary action to replenish the stock.<br><br>
        Regards,<br>
        Inventory Management Team
    """
    
    try:
        frappe.sendmail(
            recipients=recipient,
            subject=subject,
            message=message
        )
        return f"Email sent successfully to {recipient}"
    except Exception as e:
        frappe.log_error(f"Error sending email to {recipient}: {str(e)}")
        return f"Failed to send email to {recipient}. Check logs for details."


def check_reorder_levels():
    try:
        frappe.logger().info("Scheduled task started: check_reorder_levels")
        
        reorder_items = frappe.get_all(
            "Reorder Notifications",
            filters={"current_quantity": ["<", frappe.utils.cint("reorder_level")], "email_sent": 0},
            fields=["name", "item_code", "current_quantity", "reorder_level", "notification_recipient"]
        )

        frappe.logger().info(f"Fetched {len(reorder_items)} items for reorder notifications.")

        for item in reorder_items:
            if item.get("notification_recipient"):
                send_reorder_notification_email(
                    recipient=item["notification_recipient"],
                    item_name=item["item_code"],
                    current_quantity=item["current_quantity"],
                    reorder_level=item["reorder_level"]
                )
                frappe.db.set_value("Reorder Notifications", item["name"], "email_sent", 1)
                frappe.logger().info(f"Notification sent for item {item['item_code']} to {item['notification_recipient']}.")

        frappe.db.commit()
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in Reorder Notification Job")
        frappe.logger().error(f"Error in Reorder Notification Job: {str(e)}")
