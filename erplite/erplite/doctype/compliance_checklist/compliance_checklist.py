# Copyright (c) 2023, T4G Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import *
from frappe import _
from erplite.erplite.utils import *
from frappe.utils.user import get_users_with_role
from frappe.model.document import Document

class ComplianceChecklist(Document):
	def validate(self):
		validate_due_dates(self)
		change_compliance_status(self)

@frappe.whitelist()
def validate_due_dates(self):
	if getdate(self.due_date) < getdate(self.posting_date):
		frappe.throw(
			title = _('ALERT !!'),
			msg = _('Cannot select Past date in To date !')
		)

@frappe.whitelist()
def daily_compliance_scheduler():
	current_date = getdate(today())
	checklists = frappe.db.get_all('Compliance Checklist', filters = { 'status': 'Open', 'remind_before_unit': 'Day'})
	if checklists:
		for checklist in checklists:
			users = []
			checklist_doc = frappe.get_doc('Compliance Checklist', checklist.name)
			if checklist_doc.due_date:
				due_date = getdate(checklist_doc.due_date)
				if checklist_doc.role_to_notify:
					users = get_users_with_role(checklist_doc.role_to_notify)
				checklist_url = get_url_to_form(checklist_doc.doctype, checklist_doc.name)
				checklist_due_message_mail = 'Compliance Checklist '+ checklist_doc.name + ' for '+ checklist_doc.subject + ' had Overdue on '+ str(checklist_doc.due_date) + '\nReference : ' + checklist_url

				# Changing Status to Overdue and notifications
				if due_date<current_date:
					change_compliance_status(checklist_doc)
					for user in users:
						create_notification_log(checklist_doc.subject+ 'is Overdue', user, checklist_due_message_mail, checklist_doc.doctype, checklist_doc.name)

				#Daily Scheduler Checking and notifications
				if checklist_doc.remind_before:
					notification_date = frappe.utils.add_to_date(due_date, days=-1*checklist_doc.remind_before)
				else:
					notification_date = due_date
				if getdate(notification_date) == current_date:
					for user in users:
						create_notification_log(checklist_doc.subject, user, checklist_doc.description, checklist_doc.doctype, checklist_doc.name)


@frappe.whitelist()
def monthly_compliance_scheduler():
	current_date = getdate(today())
	checklists = frappe.db.get_all('Compliance Checklist', filters = { 'status': 'Open', 'remind_before_unit': 'Month'})
	if checklists:
		for checklist in checklists:
			users = []
			checklist_doc = frappe.get_doc('Compliance Checklist', checklist.name)
			if checklist_doc.due_date:
				due_date = getdate(checklist_doc.due_date)
				if checklist_doc.role_to_notify:
					users = get_users_with_role(checklist_doc.role_to_notify)
				if not checklist_doc.owner in users:
					users.append(checklist_doc.owner)
				checklist_url = get_url_to_form(checklist_doc.doctype, checklist_doc.name)
				checklist_due_message_mail = 'Compliance Checklist '+ checklist_doc.name + ' for '+ checklist_doc.subject + ' had Overdue on '+ str(checklist_doc.due_date) + '\nReference : ' + checklist_url

				# Changing Status to Overdue and notifications
				if due_date<current_date:
					change_compliance_status(checklist_doc)
					for user in users:
						create_notification_log(checklist_doc.subject+ 'is Overdue', user, checklist_due_message_mail, checklist_doc.doctype, checklist_doc.name)

				#Daily Scheduler Checking and notifications
				if checklist_doc.remind_before:
					notification_date = frappe.utils.add_to_date(due_date, months=-1*checklist_doc.remind_before)
				else:
					notification_date = due_date
				if getdate(notification_date) == current_date:
					for user in users:
						create_notification_log(checklist_doc.subject, user, checklist_doc.description, checklist_doc.doctype, checklist_doc.name)
