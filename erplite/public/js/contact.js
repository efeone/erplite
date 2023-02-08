frappe.ui.form.on('Contact', {
	onload: function (frm) {
		var prev_route = frappe.get_prev_route();
		if(prev_route[1]=='Lead'){
			frappe.db.get_value('Lead', prev_route[2], 'company_name').then(r => {
				frm.set_value('company_name', r.message.company_name);
			});
		}
	}
});
