from __future__ import unicode_literals
from frappe import _
import frappe
from frappe.utils import *
from hrms.hr.doctype.leave_application.leave_application import *

@frappe.whitelist()
def last_on_leave_for_employee(employee_id=None):
    '''Method to get No of days from last day of leave taken till today.'''
    last_on_leave = 0
    current_date = getdate(today())
    if not employee_id:
        employee_id = get_employee_id_from_user()
    if frappe.db.exists('Leave Application', { 'status': 'Approved', 'employee': employee_id, 'to_date': [ '<', current_date ] }):
        last_leave_application_doc = frappe.get_last_doc('Leave Application', { 'status': 'Approved', 'employee': employee_id, 'to_date': [ '<', current_date ] }, order_by='to_date desc')
        if last_leave_application_doc.to_date:
            last_on_leave = date_diff(current_date, getdate(last_leave_application_doc.to_date))
    return last_on_leave

@frappe.whitelist()
def approved_leave_for_employee(employee_id=None):
    '''Method to get total leaves approved for future.'''
    approved_leave = 0
    current_date = getdate(today())
    if not employee_id:
        employee_id = get_employee_id_from_user()
    if frappe.db.exists('Leave Application', { 'status': 'Approved', 'employee': employee_id, 'from_date': [ '>=', current_date ] }):
        approved_leave_applications = frappe.db.get_list('Leave Application', { 'status': 'Approved', 'employee': employee_id, 'from_date': [ '>=', current_date ] })
        if approved_leave_applications:
            approved_leave = len(approved_leave_applications)
    return approved_leave


@frappe.whitelist()
def total_leave_taken_for_employee(employee_id=None):
    '''Method to get how much leave taken since the beginning of the year till today.'''
    total_leave_taken = 0
    current_date = getdate(today())
    year_start_date = getdate(today()).replace(month=1, day=1)
    if not employee_id:
        employee_id = get_employee_id_from_user()
    if frappe.db.exists('Leave Application', { 'status': 'Approved', 'employee': employee_id, 'from_date': [ '>=', year_start_date ], 'to_date': [ '<=', current_date ] }):
        approved_leave_applications = frappe.db.get_list('Leave Application', { 'status': 'Approved', 'employee': employee_id, 'from_date': [ '>=', year_start_date ], 'to_date': [ '<=', current_date ] })
        if approved_leave_applications:
            total_leave_taken = len(approved_leave_applications)
    return total_leave_taken

@frappe.whitelist()
def remaining_leaves_for_employee(employee_id=None):
    '''Method to get remaining leaves for this year.'''
    remaining_leaves = 0
    current_date = getdate(today())
    if not employee_id:
        employee_id = get_employee_id_from_user()
    leave_allocation_records = get_leave_allocation_records(employee_id, current_date)
    for leave_allocation in leave_allocation_records:
        remaining_leaves += get_leave_balance_on(employee_id, leave_allocation, current_date, consider_all_leaves_in_the_allocation_period=True)
    return remaining_leaves

@frappe.whitelist()
def get_employee_id_from_user(user_id=None):
    ''' Method to get employee_id of specified user or logged in user '''
    employee_id = False
    if not user_id:
        user_id = frappe.session.user
    if frappe.db.exists('Employee', { 'user_id': user_id }):
        employee_id = frappe.db.get_value('Employee', { 'user_id': user_id }, 'name')
    return employee_id

@frappe.whitelist()
def change_compliance_status(self):
    '''Method to change Status of Compliance'''
    if self.status == 'Open':
        current_date = getdate(today())
        due_date = getdate(self.due_date)
        if current_date >= due_date:
            frappe.db.set_value(self.doctype, self.name, 'status', 'Overdue')
            frappe.db.commit()

@frappe.whitelist()
def create_notification_log(subject, for_user, email_content, document_type, document_name):
    notification_doc = frappe.new_doc('Notification Log')
    notification_doc.subject = subject
    notification_doc.type = 'Mention'
    notification_doc.for_user = for_user
    notification_doc.email_content = email_content
    notification_doc.document_type = document_type
    notification_doc.document_name = document_name
    notification_doc.save()
    frappe.db.commit()
