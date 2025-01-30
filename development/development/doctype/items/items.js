// Copyright (c) 2025, sreejani and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Items", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Items', {
    item_name: function (frm) {
        if (frm.doc.item_name) {
            frappe.db.get_list('Category', {
                fields: ['name', 'category_name']
            }).then(categories => {
                let matchedCategory = null; 
                let debugMessages = []; 

                let promises = categories.map(category => {
                    return frappe.db.get_list('Items List', {
                        fields: ['item_name'],  
                        filters: { parent: category.name }
                    }).then(itemsList => {
                        const itemNamesInChildTable = itemsList.map(item => item.item_name);
                        debugMessages.push(
                            `Category: ${category.category_name}\nItems in Child Table: ${itemNamesInChildTable.join(', ') || 'No Items'}`
                        );

                        if (itemNamesInChildTable.includes(frm.doc.item_name)) {
                            matchedCategory = category.category_name;
                        }
                    });
                });

                Promise.all(promises).then(() => {
                    if (matchedCategory) {
                        frm.set_value('category', matchedCategory);
                        frappe.msgprint({
                            title: 'Category Matched',
                            // message: `Item "${frm.doc.item_name}" found in category "${matchedCategory}".`,
                            indicator: 'green'
                        });
                    } else {
                        frm.set_value('category', categories[0].category_name);  
                        // frappe.msgprint({
                        //     // message: `Item "${frm.doc.item_name}" not found in any category. Defaulting to "${categories[0].category_name}".`,
                        // });
                    }

                    // frappe.msgprint({
                    //     // message: debugMessages.join('<br><br>'),
                    // });
                });
            });
        } else {
            frm.set_value('category', null);
            // frappe.msgprint({
            //     // message: 'Please enter an item name to fetch the category.',
            // });
        }
    }
});
