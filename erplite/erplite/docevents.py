from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import *

def leave_application_validate(doc, method):
    if doc.status != 'Open' and doc.owner == frappe.session.user:
        frappe.throw(
            _("You're not able to Approve/Reject your own Leave Application {0}. Please contact Leave Approver.").format(frappe.bold(doc.name))
        )

def expense_claim_validate(doc, method):
    if doc.approval_status != 'Draft' and doc.owner == frappe.session.user:
        frappe.throw(
            _("You're not able to Approve/Reject your own Expense Claim {0}. Please contact Expense Approver.").format(frappe.bold(doc.name))
        )

def expense_claim_on_update_after_submit(doc, method):
    notify_employee_on_claim(doc)
    if doc.workflow_state == 'Payment Done' and doc.status != 'Paid':
        frappe.throw(
            _("Payment is not yet done for Expense Claim {0}. Please create Payment first.").format(frappe.bold(doc.name))
        )

def expense_claim_on_submit(doc, method):
    notify_employee_on_claim(doc)

def notify_employee_on_claim(self):
    ''' Method to notify Employee on status of Expense Claim '''
    employee = frappe.get_doc("Employee", self.employee)
    if not employee.user_id:
        return

    parent_doc = frappe.get_doc("Expense Claim", self.name)
    args = parent_doc.as_dict()

    template = frappe.db.get_single_value("ERPLite Settings", "expense_claim_status_notification_template")
    if not template:
        frappe.msgprint(_("Please set default template for Expense Claim Status Notification in ERPLite Settings."))
        return
    email_template = frappe.get_doc("Email Template", template)
    message = frappe.render_template(email_template.response, args)

    args = {
        # for post in messages
        "message": message,
        "message_to": employee.user_id,
        # for email
        "subject": email_template.subject,
        "notify": "employee",
    }
    notify(self, args)

def notify(self, args):
    args = frappe._dict(args)
    # args -> message, message_to, subject
    contact = args.message_to
    if not isinstance(contact, list):
        if not args.notify == "employee":
            contact = frappe.get_doc("User", contact).email or contact

    sender = dict()
    sender["email"] = frappe.get_doc("User", frappe.session.user).email
    sender["full_name"] = get_fullname(sender["email"])

    try:
        frappe.sendmail(
            recipients=contact,
            sender=sender["email"],
            subject=args.subject,
            message=args.message,
        )
        frappe.msgprint(_("Email sent to {0}").format(contact))
    except frappe.OutgoingEmailError:
        pass

@frappe.whitelist()
def set_bank_account_count(doc, method):
    no_of_local_accounts = 0
    no_of_fcra_accounts = 0
    total_count = 0
    company = frappe.defaults.get_user_default("Company")
    if company:
        total_count = get_bank_account_count()
        no_of_fcra_accounts = get_bank_account_count('FCRA Account')
        no_of_local_accounts = get_bank_account_count('Local Currency Account')
        frappe.db.set_value('Company', company, 'no_of_local_accounts', no_of_local_accounts, update_modified=False)
        frappe.db.set_value('Company', company, 'no_of_fcra_accounts', no_of_fcra_accounts, update_modified=False)
        frappe.db.set_value('Company', company, 'total_number_of_bank_accounts', total_count, update_modified=False)

@frappe.whitelist()
def get_bank_account_count(account_type=None):
    count = 0
    if account_type:
        if frappe.db.exists('Bank Account', { 'account_type': account_type }):
            count = frappe.db.count('Bank Account', { 'account_type': account_type })
    else:
        count = frappe.db.count('Bank Account')
    return count
