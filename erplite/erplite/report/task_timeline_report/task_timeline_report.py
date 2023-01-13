# Copyright (c) 2023, T4G Labs and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cstr, flt, formatdate, getdate
from erplite.erplite.report.task_time_line_report import filter_tasks


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{'label': _('Task'), 'fieldtype': 'Link', 'options': 'Task', 'width': 250},
		{'label': _('Subject'), 'fieldtype': 'Data', 'width': 350},
		{'label': _('Project'), 'fieldtype': 'Link', 'options': 'Project', 'width': 350},
		{'label': _('Project Name'), 'fieldtype': 'Data', 'hidden': 1, 'width': 0},
		{'label': _('Status'), 'fieldtype': 'Data', 'width': 200},
		{'label': _('Start Date'), 'fieldtype': 'Date', 'width': 150},
		{'label': _('End Date'), 'fieldtype': 'Date', 'width': 150},
		{'label': _('Progress'), 'fieldtype': 'Data', 'width': 150},
	]
	return columns

def get_data(filters=None):
	data=[]
	if filters.project:
		tasks = frappe.db.sql(
			"""select name, subject, parent_task, project, status, exp_start_date, exp_end_date, progress, lft, rgt

			from `tabTask` where project=%s order by lft""",
			filters.project,
			as_dict=True
		)
	else:
		tasks = frappe.db.sql(
			"""select name, subject, parent_task, project, status, exp_start_date, exp_end_date, progress, lft, rgt

			from `tabTask` order by lft""",
			as_dict=True
		)
	if not tasks:
		return None
	tasks, tasks_by_name, parent_children_map = filter_tasks(tasks)
	min_lft, max_rgt = frappe.db.sql(
		"""select min(lft), max(rgt) from `tabTask`
		where project=%s""",
		(filters.project)
	)[0]
	total_row = []
	data = prepare_data(tasks, filters, total_row, parent_children_map)
	return data

def prepare_data(tasks, filters, total_row, parent_children_map):
	data = []
	for task in tasks:
		project_name = ""
		if task.project:
			project_name = frappe.db.get_value('Project', task.project, 'project_name')
		row = {
			"task": task.name,
			"parent_task": task.parent_task,
			"indent": task.indent,
			"task": task.name,
			"subject": task.subject,
			"project": task.project,
			"project_name": project_name,
			"status": task.status,
			"start_date": task.exp_start_date,
			"end_date": task.exp_end_date,
			"progress": task.progress,
		}
		data.append(row)
	return data
