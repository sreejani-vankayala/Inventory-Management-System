import frappe
from frappe.email.queue import flush

def check_and_send_reorder_notifications():
    """Scheduled job to check reorder levels, send emails, and trigger sending automatically."""

    low_stock_items = frappe.get_all(
        "Reorder Notifications",
        filters={"reorder_level": ["<", 30]},  
        fields=["name", "item_code", "current_quantity", "reorder_level", "notification_recipient"]
    )

    if not low_stock_items:
        frappe.logger().info("No low-stock items found.")
        return
    
    for item in low_stock_items:
        if not item.notification_recipient:
            frappe.logger().warning(f"No recipient found for item {item.item_code}")
            continue  
        
        subject = f"Reorder Notification for {item.item_code}"
        message = f"""
        <p>Dear User,</p>
        <p>The stock level for the item <b>{item.item_code}</b> has fallen below the reorder level of <b>{item.reorder_level}</b>.</p>
        <p>Please take necessary action to replenish the stock.</p>
        <br>
        <p>Regards,<br>Inventory Management Team</p>
        """

        try:
            frappe.sendmail(
                recipients=item.notification_recipient,
                subject=subject,
                message=message
            )
            frappe.logger().info(f"Email queued for {item.notification_recipient} regarding {item.item_code}")

            frappe.db.set_value("Reorder Notifications", item.name, "email_sent", 1)

        except Exception as e:
            frappe.log_error(f"Error sending email to {item.notification_recipient}: {str(e)}")
            frappe.logger().error(f"Failed to queue email for {item.item_code}: {str(e)}")

    frappe.enqueue(method=flush, queue="short")
    frappe.logger().info("Email queue flushed and emails sent.")

    frappe.db.commit()
