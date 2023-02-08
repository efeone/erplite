frappe.ui.form.on("Expense Claim", {
  setup: function(frm){
    set_filters(frm);
    frm.set_df_property('approval_status', 'read_only', 1);
    frm.refresh_field('approval_status');
  },
  refresh: function(frm) {
    set_filters(frm);
    frm.set_df_property('approval_status', 'read_only', 1);
    frm.refresh_field('approval_status');
    if (!frm.is_new()){
      if (frm.doc.approval_status=='Draft' && ( frappe.user.has_role('Accounts Manager') || frappe.user.has_role('Expense Approver')) && frappe.session.user!= frm.doc.owner ){
        frm.set_df_property('expense_approver', 'read_only', 0);
      }else {
        frm.set_df_property('expense_approver', 'read_only', 1);
      }
    }
    else {
      frm.set_value('approval_status', 'Draft');
    }
  },
  travel_request: function(frm){
    if(frm.doc.travel_request){
      set_expenses_from_travel_request(frm, frm.doc.travel_request);
    }
  }
});

function set_filters(frm) {
  frm.set_query("travel_request", function() {
    return {
      "filters": {
        "docstatus": 1,
        "employee": frm.doc.employee
      }
    };
  });
}

function set_expenses_from_travel_request(frm, travel_request){
  if(travel_request){
    frappe.db.get_doc('Travel Request', travel_request).then(doc => {
      if(doc.costings){
        frm.clear_table('expenses');
        frm.refresh_field('expenses');
        doc.costings.forEach(costing => {
          let expense = frm.add_child('expenses');
          expense.expense_date = frm.doc.posting_date;
          expense.expense_type = costing.expense_type;
          expense.description = costing.comments;
          expense.amount = costing.total_amount;
          expense.sanctioned_amount = costing.total_amount;
        });
        frm.refresh_field('expenses');
      }
    });
  }
}
