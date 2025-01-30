# Copyright (c) 2025, sreejani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Source(Document):
	pass

@frappe.whitelist()
def update_destination(full_name):
    """
    Update the Destination doctype with the given full_name from Source.
    """
    # Check if a record already exists in Destination with the same full_name
    existing_record = frappe.db.exists("Destination", {"full_name": full_name})
    
    if not existing_record:
        # Create a new record in Destination doctype
        destination_doc = frappe.get_doc({
            "doctype": "Destination",
            "full_name": full_name
        })
        destination_doc.insert()
        frappe.db.commit()
        return {"status": "success", "message": f"Record inserted for {full_name} in Destination doctype."}
    else:
        return {"status": "exists", "message": f"Record already exists for {full_name} in Destination doctype."}