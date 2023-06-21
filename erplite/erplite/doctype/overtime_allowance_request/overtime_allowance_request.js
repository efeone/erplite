// Copyright (c) 2023, T4G Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Allowance Request', {
	refresh: function(frm) {
		let roles = frappe.user_roles;
    if(frm.doc.docstatus == 1 && frm.doc.workflow_state == 'Approved' && frm.doc.leaves_allocated == 0 && roles.includes('HR Manager')){
      frm.add_custom_button('Allocate Additional Leaves', () => {
        allocate_additional_leave(frm);
      }).addClass("btn btn-primary");
    }
	}
});

let allocate_additional_leave = function(frm){
  let d = new frappe.ui.Dialog({
    title: 'Allocate Additional Leaves',
    fields: [
        {
            label: 'Leave Type',
            fieldname: 'leave_type',
            fieldtype: 'Link',
            options: 'Leave Type',
            reqd: 1,
            get_query : function() {
							return {
								filters: {
									is_compensatory: 1
								}
							}
						}
        },
        {
            label: 'No. of Days',
            fieldname: 'no_of_days',
            fieldtype: 'Int',
            reqd: 1
        }
    ],
    primary_action_label: 'Allocate',
    primary_action(values) {
			frappe.call({
				method : 'erplite.erplite.doctype.overtime_allowance_request.overtime_allowance_request.allocate_leaves',
				args: {
					docname: frm.doc.name,
	        leave_type: values.leave_type,
	        no_of_days: values.no_of_days
				},
				freeze: true,
				callback: (r) => {
					frm.reload_doc()
				},
			});
      d.hide();
    }
  });
  d.show();
}
