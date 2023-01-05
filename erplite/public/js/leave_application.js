frappe.ui.form.on("Leave Application", {
  refresh: function(frm) {
    if (!frm.is_new()){
      // check approvers
      if ((frm.doc.status=='Open' && frappe.session.user!=frm.doc.leave_approver) || frappe.session.user == frm.doc.owner){
        $('.primary-action').hide();
        frm.set_df_property('status', 'read_only', 1);
        frm.set_df_property('leave_approver', 'read_only', 1);
      }
      if (frm.doc.status=='Open' && frappe.user.has_role('HR Manager') && frappe.session.user!= frm.doc.owner ){
        $('.primary-action').show();
        frm.set_df_property('status', 'read_only', 0);
        frm.set_df_property('leave_approver', 'read_only', 0);
      }
      frm.refresh_field('status');
      frm.refresh_field('leave_approver');
    }
  }
})
