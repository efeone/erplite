// Copyright (c) 2023, T4G Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Compliance Checklist', {
  due_date: function(frm){
    if(frm.doc.due_date < frm.doc.posting_date){
      frappe.throw({title:'ALERT !!',message: 'Cannot select past date in To date!'})
    }
  }
});
