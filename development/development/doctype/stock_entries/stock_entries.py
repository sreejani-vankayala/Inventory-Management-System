# Copyright (c) 2025, sreejani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StockEntries(Document):
	pass


def update_stock_ledger_after_insert(doc, method):
    
    try:
        item_code = doc.item_code
        item_name = doc.item_name
        item_group = doc.item_group
        default_warehouse = doc.default_warehouse

        existing_record = frappe.db.exists("Stock Ledger", {"item_code": item_code})
        
        if not existing_record:
            stock_ledger_doc = frappe.get_doc({
                "doctype": "Stock Ledger",
                "item_code": item_code,
                "item_name": item_name,
                "item_group": item_group,
                "warehouse": default_warehouse
            })
            stock_ledger_doc.insert()
            frappe.db.commit()
            frappe.msgprint(f"Record inserted for {item_code} in Stock Ledger doctype.")
        else:
            frappe.msgprint(f"Record already exists for {item_code} in Stock Ledger doctype.")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Stock Ledger Insert Error")
        frappe.throw(f"An error occurred: {e}")

