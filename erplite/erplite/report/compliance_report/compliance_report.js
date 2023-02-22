// Copyright (c) 2023, T4G Labs and contributors
// For license information, please see license.txt

frappe.query_reports["Compliance Report"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": '\nOpen\nCancelled\nOverdue\nOn Hold\nCompleted'
		}
	]
};
