// Copyright (c) 2023, T4G Labs and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Expense Claim Summary"] = {
	"filters": [
		{
			'fieldname': 'from_date',
			'label': __('From Date'),
			'fieldtype': 'Date',
			'default': frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			'reqd': 1
		},
		{
			'fieldname': 'to_date',
			'label': __('To Date'),
			'fieldtype': 'Date',
			'default': frappe.datetime.get_today(),
			'reqd': 1
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": 'Employee'
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": '\nPending\nPayment Done\nRejected\nApproved'
		},
	]
};
