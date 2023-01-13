// Copyright (c) 2023, T4G Labs and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Task Timeline Report"] = {
	"filters": [
		{
		"fieldname": "project",
		"label": __("Project"),
		"fieldtype": "Link",
		"options": "Project"
		}
	],
	"tree": true,
	"treeView": true,
	"name_field": "task",
	"parent_field": "parent_task",
	"initial_depth": 3
};
