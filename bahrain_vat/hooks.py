from . import __version__ as app_version

app_name = "bahrain_vat"
app_title = "BAHRAIN VAT"
app_publisher = "ERPGulf"
app_description = "BAHRAIN VAT Management and Reporting"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "support@erpgulf.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bahrain_vat/css/bahrain_vat.css"
# app_include_js = "/assets/bahrain_vat/js/bahrain_vat.js"

# include js, css files in header of web template
# web_include_css = "/assets/bahrain_vat/css/bahrain_vat.css"
# web_include_js = "/assets/bahrain_vat/js/bahrain_vat.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bahrain_vat/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
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

# Installation
# ------------

# before_install = "bahrain_vat.install.before_install"
# after_install = "bahrain_vat.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bahrain_vat.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Company": {
        "on_update": "bahrain_vat.bahrain_vat.setup.operations.setup_bahrain_vat_setting.create_bahrain_vat_setting",
        "on_update": "bahrain_vat.bahrain_vat.setup.operations.setup_bahrain_vat_setting.make_custom_fields"
        
        
    },
    "Sales Invoice": {
        "after_insert": "bahrain_vat.events.accounts.sales_invoice.create_qr_code",
        "on_trash": "bahrain_vat.events.accounts.sales_invoice.delete_qr_code_file"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"bahrain_vat.tasks.all"
# 	],
# 	"daily": [
# 		"bahrain_vat.tasks.daily"
# 	],
# 	"hourly": [
# 		"bahrain_vat.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bahrain_vat.tasks.weekly"
# 	]
# 	"monthly": [
# 		"bahrain_vat.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "bahrain_vat.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "bahrain_vat.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "bahrain_vat.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"bahrain_vat.auth.validate"
# ]

fixtures = [
    {
        'dt': 'Custom Field',
        'filters': {
            'name': ['in', [
                'Sales Invoice-qr_code',
                'Company-company_name_in_arabic',
                'Supplier-supplier_name_in_arabic',
                'Sales Invoice-customer_name_in_arabic',
                'Purchase Order-supplier_name_in_arabic',
                'Item-is_zero_rated',
                'Item-is_exempt',
                'Address-address_in_arabic',
                'Customer-customer_name_in_arabic',
                'Contact-is_billing_contact',
                'Item-tax_code',
                'Purchase Invoice-supplier_name_in_arabic'
                
            ]]
        }
    }
]

jenv = {
    'methods': [
        'string_to_json:bahrain_vat.jinja.utils.string_to_json'
    ]
}
