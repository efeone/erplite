from . import __version__ as app_version

app_name = "erplite"
app_title = "ERPLite"
app_publisher = "T4G Labs"
app_description = "ERPLite for Changemakers"
app_email = "sherin@efeone.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erplite/css/erplite.css"
# app_include_js = "/assets/erplite/js/erplite.js"

# include js, css files in header of web template
# web_include_css = "/assets/erplite/css/erplite.css"
# web_include_js = "/assets/erplite/js/erplite.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "erplite/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
        "Leave Application" : "public/js/leave_application.js",
        "Expense Claim" : "public/js/expense_claim.js",
        "Contact" : "public/js/contact.js",
        "Event" : "public/js/event.js"
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "erplite.utils.jinja_methods",
#	"filters": "erplite.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "erplite.install.before_install"
# after_install = "erplite.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "erplite.uninstall.before_uninstall"
# after_uninstall = "erplite.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erplite.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Leave Application": {
		"validate": "erplite.erplite.docevents.leave_application_validate",
	},
    "Expense Claim": {
		"validate": "erplite.erplite.docevents.expense_claim_validate",
        "on_submit": "erplite.erplite.docevents.expense_claim_on_submit",
        "on_update_after_submit": "erplite.erplite.docevents.expense_claim_on_update_after_submit"
	},
    "Bank Account": {
		"on_update": "erplite.erplite.docevents.set_bank_account_count",
		"on_trash": "erplite.erplite.docevents.set_bank_account_count"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"erplite.erplite.doctype.compliance_checklist.compliance_checklist.daily_compliance_scheduler"
	],
    "monthly": [
		"erplite.erplite.doctype.compliance_checklist.compliance_checklist.monthly_compliance_scheduler"
	]
}

# scheduler_events = {
#	"all": [
#		"erplite.tasks.all"
#	],
#	"daily": [
#		"erplite.tasks.daily"
#	],
#	"hourly": [
#		"erplite.tasks.hourly"
#	],
#	"weekly": [
#		"erplite.tasks.weekly"
#	],
#	"monthly": [
#		"erplite.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "erplite.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "erplite.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "erplite.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"erplite.auth.validate"
# ]

fixtures = [
		{"dt": "Role", "filters": [["name", "in", ["Changemaker User", "Compliance User"]]]},
        {"dt": "Email Template", "filters": [["name", "in", ["Expense Claim Status Notification", "Expense Claim Approval Notification"]]]},
        {"dt": "Workflow State", "filters": [["name", "in", ["Pending", "Payment Done", "Rejected", "Approved"]]]},
        {"dt": "Workflow", "filters": [["name", "in", ["Expense Claim"]]]},
		{"dt": "Bank Account Type", "filters": [["name", "in", ["FCRA Account", "Local Currency Account"]]]},
	]
