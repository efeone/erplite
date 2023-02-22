# Copyright (c) 2023, T4G Labs and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	return[
		_("Compliance") + ":Link/Compliance Checklist:150",
		_("Subject") + ":Data:600",
		_("Due Date") + ":Date:150",
		_("Status") + ":Data:150",
		_("Assigned Role") + ":Link/Role:150",
		_("Assigned To") + ":Data:350",
	]

def get_data(filters):
	data = []
	if filters.get('status'):
		compliance_list = frappe.get_all('Compliance Checklist', { 'status':filters.get('status') })
	else:
		compliance_list = frappe.get_all('Compliance Checklist')
	if compliance_list:
		for compliance in compliance_list:
			doc = frappe.get_doc('Compliance Checklist', compliance.name)
			users = doc._assign
			if users:
				assigned_to = make_assign_to(format_text(users[1:-1]))
			else:
				assigned_to = " "
			row = [
				doc.name,
				doc.subject,
				doc.due_date,
				doc.status,
				doc.role_to_notify,
				assigned_to
			]
			data.append(row)
	return data

def make_assign_to(users):
	assigned_to = 0
	user_list = users.split(',')
	for user in user_list:
		if frappe.db.exists('User', user):
			user_name = frappe.db.get_value('User', user, 'full_name')
		else:
			user_name = ''
		if assigned_to:
			assigned_to = assigned_to + ', ' + user_name
		else:
			assigned_to = user_name
	return assigned_to

def format_text(text):
	format_text = text.replace('"', '')
	formatted_text = format_text.replace(' ', '')
	return formatted_text
