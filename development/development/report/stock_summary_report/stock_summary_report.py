# Copyright (c) 2025, sreejani and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


import frappe

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "item_code", "label": "Item Code", "fieldtype": "Data", "width": 150},
        {"fieldname": "item_name", "label": "Item Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "warehouse", "label": "Warehouse", "fieldtype": "Data", "width": 150},
        {"fieldname": "warehouse_reorder_level", "label": "Reorder Level", "fieldtype": "Float", "width": 120},
    ]

def get_data(filters):

    conditions = []
    if filters.get("item_name"):
        conditions.append(f"items.item_name LIKE '%{filters.get('item_name')}%'")
    if filters.get("warehouse"):
        conditions.append(f"reorder.warehouse = '{filters.get('warehouse')}'")

    conditions_query = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT
            items.item_code,
            items.item_name,
            reorder.warehouse,
            reorder.warehouse_reorder_level
        FROM
            `tabItems` items
        INNER JOIN
            `tabItem Reorder` reorder ON items.name = reorder.parent
        WHERE
            {conditions_query}
    """
    data = frappe.db.sql(query, as_dict=True)
    return data
