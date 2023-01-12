# Copyright (c) 2023, T4G Labs and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from erplite.erplite.utils import *

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	return[
		_("Employee") + ":Link/Employee:200",
		_("Employee Name") + ":Data:150",
		_("Last on Leave") + ":Int:150",
		_("Approved Leave") + ":Int:150",
		_("Total Leave taken") + ":Int:150",
		_("Remaining Leaves") + ":Int:150",
	]

def get_data(filters):
	data=[]
	if not filters.get('employee'):
		if frappe.session.user:
			user_id = frappe.session.user
			if user_id == 'Administrator':
				data = prepare_data_for_all_employees()
			else:
				if 'HR Manager' in frappe.get_roles(user_id):
					data = prepare_data_for_all_employees()
				else:
					employee_id = get_employee_id_from_user(user_id)
					if employee_id:
						reports_to = get_reports_to_employees(employee_id)
						reports_to.append({ 'name': employee_id })
						if reports_to:
							for employee in reports_to:
								row = prepare_data_for_employee(employee.get('name'))
								data.append(row)
	else:
		employee_id = filters.get('employee')
		row = prepare_data_for_employee(employee_id)
		data.append(row)
	return data

def prepare_data_for_all_employees():
	''' Method to get leave details of all employees '''
	data = []
	employees = frappe.get_list("Employee", filters={ 'status': 'Active'})
	for employee in employees:
		employee_id = employee.name
		row = prepare_data_for_employee(employee_id)
		data.append(row)
	return data

def prepare_data_for_employee(employee_id):
	''' Method to get leave details of employee '''
	employee_name = frappe.db.get_value('Employee', employee_id, 'employee_name')
	last_on_leave = last_on_leave_for_employee(employee_id)
	approved_leave = approved_leave_for_employee(employee_id)
	total_leave_taken = total_leave_taken_for_employee(employee_id)
	remaining_leaves = remaining_leaves_for_employee(employee_id)
	row = [
		employee_id,
		employee_name,
		last_on_leave,
		approved_leave,
		total_leave_taken,
		remaining_leaves
	]
	return row

def get_reports_to_employees(employee_id):
	''' Method to get all employees who are reporting to this employee '''
	reports_to = frappe.db.get_all("Employee", filters={"reports_to": employee_id, "status": "Active"})
	return reports_to
