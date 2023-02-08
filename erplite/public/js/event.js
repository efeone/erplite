frappe.ui.form.on('Event', {
	validate: function (frm) {
    if(frm.doc.event_participants){
      frm.doc.event_participants.forEach(event_participant => {
        if(!event_participant.email){
          if(event_participant.reference_doctype == 'Employee'){
            frappe.db.get_value(event_participant.reference_doctype, event_participant.reference_docname, 'prefered_email').then(r => {
              event_participant.email = r.message.prefered_email;
            });
          }
        }
      });
      frm.refresh_field('event_participants');
    }
	}
});

frappe.ui.form.on('Event Participants', {
	reference_docname: function(frm, cdt, cdn) {
    var row=locals[cdt][cdn];
    if(row.reference_doctype == 'Employee'){
      frappe.db.get_value(row.reference_doctype, row.reference_docname, 'prefered_email').then(r => {
        frappe.model.set_value(row.doctype, row.name, 'email', r.message.prefered_email);
      });
    }
    frm.refresh_field('event_participants');
	}
});
