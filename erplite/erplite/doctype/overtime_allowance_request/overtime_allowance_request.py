# Copyright (c) 2023, T4G Labs and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import datetime

class OvertimeAllowanceRequest(Document):
	pass

@frappe.whitelist()
def allocate_leaves(docname, leave_type, no_of_days):
	if float(no_of_days)<1:
		frappe.throw('No of days should be greater than or equal to 1!')
	else:
		employee, employee_name, posting_date = frappe.db.get_value('Overtime Allowance Request', docname, ['employee', 'employee_name', 'posting_date'])
		from_date = getdate(posting_date)
		to_date = getdate(datetime(from_date.year, 12, 31).strftime('%Y-%m-%d'))
		if employee and employee_name:
			if frappe.db.exists('Leave Allocation', { 'employee': employee, 'leave_type':leave_type, 'expired':0, 'docstatus':['<', 2] }):
				leave_allocation = frappe.get_last_doc('Leave Allocation', { 'employee': employee, 'leave_type':leave_type, 'expired':0, 'docstatus':['<', 2] })
				leave_allocation.new_leaves_allocated = float(leave_allocation.new_leaves_allocated) + float(no_of_days)
				leave_allocation.save()
				leave_allocation.add_comment('Comment', "Compensatory Leave added against Overtime Allowance Request : {} ".format(docname))
			else:
				leave_allocation = frappe.new_doc('Leave Allocation')
				leave_allocation.employee = employee
				leave_allocation.leave_type = leave_type
				leave_allocation.from_date = from_date
				leave_allocation.to_date = to_date
				leave_allocation.new_leaves_allocated = float(no_of_days)
				leave_allocation.submit()
				leave_allocation.add_comment('Comment', "Compensatory Leave added against Overtime Allowance Request : {} ".format(docname))
			frappe.db.set_value('Overtime Allowance Request', docname, 'leaves_allocated', 1)
			frappe.db.commit()
			frappe.msgprint('Leave Allocated successfully', alert=True, indicator='green')
		else:
			frappe.throw('Employee is Missing!')
