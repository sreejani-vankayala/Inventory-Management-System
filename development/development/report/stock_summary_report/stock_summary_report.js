// Copyright (c) 2025, sreejani and contributors
// For license information, please see license.txt

// frappe.query_reports["Stock Summary Report"] = {
// 	"filters": [

// 	]
// };

frappe.query_reports["Stock Summary Report"] = {
    filters: [
        {
            fieldname: "item_name",
            label: __("Item Name"),
            fieldtype: "Link",
			options: "Items",
            reqd: 0,
            default: "",
        },
        {
            fieldname: "warehouse",
            label: __("Warehouse"),
            fieldtype: "Link",
            options: "Warehouse",
            reqd: 0,
            default: "",
        },
    ],
};

