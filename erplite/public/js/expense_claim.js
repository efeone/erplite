frappe.ui.form.on("Expense Claim", {
  setup: function(frm){
    frm.set_df_property('approval_status', 'read_only', 1);
    frm.refresh_field('approval_status');
  },
  refresh: function(frm) {
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
  }
})
