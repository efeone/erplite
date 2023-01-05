from __future__ import unicode_literals
import frappe
from frappe import _

@frappe.whitelist()
def leave_application_validate(doc, method):
    if doc.status != 'Open' and doc.owner == frappe.session.user:
        frappe.throw(
            _("You're not able to Approve/Reject your own Leave Application. Please contact Leave Approver {0}.").format(frappe.bold(doc.name))
        )
