# Copyright (c) 2025, sreejani and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

import frappe
from frappe.utils import getdate, add_days, nowdate

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "transaction_date", "label": "Transaction Date", "fieldtype": "Date", "width": 120},
        {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"fieldname": "item_code", "label": "Item Code", "fieldtype": "Link", "options": "Item", "width": 150},
        {"fieldname": "item_name", "label": "Item Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "item_group", "label": "Item Group", "fieldtype": "Link", "options": "Item Group", "width": 150},
        {"fieldname": "quantity", "label": "Quantity", "fieldtype": "Float", "width": 120},
        {"fieldname": "source_warehouse", "label": "Source Warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        {"fieldname": "target_warehouse", "label": "Target Warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
    ]

def get_data(filters):

    filters = filters or {}
    if not filters.get("from_date"):
        filters["from_date"] = getdate(add_days(nowdate(), -365)).replace(month=12, day=1)
    if not filters.get("to_date"):
        filters["to_date"] = nowdate()

    conditions = {
        "transaction_date": ["between", [filters["from_date"], filters["to_date"]]],
    }

    if filters.get("company"):
        conditions["company"] = filters["company"]
    if filters.get("warehouse"):
        conditions["source_warehouse"] = filters["warehouse"]
        conditions["target_warehouse"] = filters["warehouse"]
    if filters.get("item_name"):
        conditions["item_name"] = ["like", f"%{filters['item_name']}%"]
    if filters.get("item_group"):
        conditions["item_group"] = filters["item_group"]

    entries = frappe.get_all(
        "Stock Ledger",
        fields=[
            "transaction_date",
            "company",
            "item_code",
            "item_name",
            "item_group",
            "quantity",
            "source_warehouse",
            "target_warehouse",
        ],
        filters=conditions,
        order_by="transaction_date, item_code"
    )

    data = []
    for entry in entries:
        data.append({
            "transaction_date": entry.transaction_date,
            "company": entry.company,
            "item_code": entry.item_code,
            "item_name": entry.item_name,
            "item_group": entry.item_group,
            "quantity": entry.quantity,
            "source_warehouse": entry.source_warehouse,
            "target_warehouse": entry.target_warehouse,
        })

    return data
