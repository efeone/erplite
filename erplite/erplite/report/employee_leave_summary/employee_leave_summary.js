// Copyright (c) 2023, T4G Labs and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Leave Summary"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": 'Employee'
		},
		{
			"fieldname":"user",
			"label": __("User"),
			"fieldtype": "Link",
			"options": 'User',
			"hidden": '1',
		}
	]
};
