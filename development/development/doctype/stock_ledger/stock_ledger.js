// Copyright (c) 2025, sreejani and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Stock Ledger", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Stock Ledger', {
    onload: function (frm) {
        frm.set_df_property('stock_value', 'read_only', 1);
    },
    quantity: function (frm) {
        update_stock_value(frm);
    },
    valuation_rate: function (frm) {
        update_stock_value(frm);
    }
});

function update_stock_value(frm) {
    const quantity = frm.doc.quantity || 0;
    const valuation_rate = frm.doc.valuation_rate || 0;

    const stock_value = quantity * valuation_rate;

    frm.set_value('stock_value', stock_value);
}

