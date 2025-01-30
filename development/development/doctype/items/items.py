# Copyright (c) 2025, sreejani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_url_to_form


class Items(Document):
	pass
 
def check_item_reorder_levels():
    items = frappe.db.sql("""
        SELECT 
            i.name AS item_name,
            i.stock_quantity,
            r.warehouse,
            r.warehouse_reorder_level
        FROM 
            `tabItems` i
        JOIN 
            `tabItem Reorder` r ON r.parent = i.name
        WHERE 
            i.stock_quantity > r.warehouse_reorder_level
    """, as_dict=True)
 
    for item in items:
        create_notification(item)
 
def create_notification(item):
    message = (
        f"Item {item.item_name} has a stock quantity of {item.stock_quantity}, "
        f"which is greater than the reorder level of {item.warehouse_reorder_level} "
        f"in warehouse {item.warehouse}. However, it is marked as below reorder level."
    )
 
    frappe.get_doc({
        "doctype": "Notification Log",
        "subject": "Stock Below Reorder Level",
        "email_content": message,
        "for_user": "Administrator", 
        "type": "Alert"
    }).insert(ignore_permissions=True)