# Copyright (c) 2023, T4G Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import *
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{'label': _('Employee'), 'fieldtype': 'Link', 'options': 'Employee', 'width': 200},
		{'label': _('Employee Name'), 'fieldtype': 'Data', 'width': 230},
		{'label': _('Posting Date'), 'fieldtype': 'Date', 'width': 130},
		{'label': _('Expense Claim'), 'fieldtype': 'Link', 'options': 'Expense Claim', 'width': 200},
		{'label': _('Claim Type'), 'fieldtype': 'Link', 'options': 'Expense Claim Type', 'width': 130},
		{'label': _('Description'), 'fieldtype': 'Data', 'width': 250},
		{'label': _('Status'), 'fieldtype': 'Data', 'width': 130},
		{'label': _('Total Amount'), 'fieldtype': 'Currency', 'width': 150},
		{'label': _('Sanctioned Amount'), 'fieldtype': 'Currency', 'width': 200}
	]
	return columns

def get_data(filters=None):
	data=[]
	expense_claim_list = frappe.db.get_all('Expense Claim', filters=get_filters(filters))
	for expense_claim in expense_claim_list:
		expense_claim_doc = frappe.get_doc('Expense Claim', expense_claim.name)
		for expense in expense_claim_doc.expenses:
			row = [
				expense_claim_doc.employee,
				expense_claim_doc.employee_name,
				expense_claim_doc.posting_date,
				expense_claim_doc.name,
				expense.expense_type,
				expense.description,
				expense_claim_doc.workflow_state,
				expense.amount,
				expense.sanctioned_amount
			]
			data.append(row)
	return data

def get_filters(filters=None):
	conditions = {}
	if filters.employee:
		conditions['employee'] = filters.employee
	if filters.from_date and filters.to_date:
		conditions['posting_date'] = [ 'between' , [ getdate(filters.from_date), getdate(filters.to_date) ] ]
	if filters.status:
		conditions['workflow_state'] = filters.status
	if conditions:
		return conditions
	else:
		return []
