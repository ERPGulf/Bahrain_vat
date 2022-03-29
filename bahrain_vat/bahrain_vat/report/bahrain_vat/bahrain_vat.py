# Copyright (c) 2022, ERPGulf and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import get_url_to_list
from erpnext.controllers.taxes_and_totals import get_itemised_tax_breakup_data, get_rounded_tax_amount
import json

def execute(filters=None):
	columns = columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "title",
			"label": _("Title"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "amount",
			"label": _("Amount (BHD)"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"fieldname": "adjustment_amount",
			"label": _("Adjustment (BHD)"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"fieldname": "vat_amount",
			"label": _("VAT Amount (BHD)"),
			"fieldtype": "Currency",
			"width": 150,
		}
	]

def get_data(filters):
	data = []

	# Validate if vat settings exist
	company = filters.get('company')
	if frappe.db.exists('BAHRAIN VAT Setting', company) is None:
		url = get_url_to_list('BAHRAIN VAT Setting')
		frappe.msgprint(f'Create <a href="{url}">BAHRAIN VAT Setting</a> for this company')
		return data

	bahrain_vat_setting = frappe.get_doc('BAHRAIN VAT Setting', company)
	
	# Sales Heading
	append_data(data, 'VAT on Sales', '', '', '')

	grand_total_taxable_amount = 0
	grand_total_taxable_adjustment_amount = 0
	grand_total_tax = 0

	for vat_setting in bahrain_vat_setting.bahrain_vat_sales_accounts:
		total_taxable_amount, total_taxable_adjustment_amount, \
			total_tax = get_tax_data_for_each_vat_setting(vat_setting, filters, 'Sales Invoice')
		
		# Adding results to data
		append_data(data, vat_setting.title, total_taxable_amount, 
			total_taxable_adjustment_amount, total_tax)
		
		grand_total_taxable_amount += total_taxable_amount
		grand_total_taxable_adjustment_amount += total_taxable_adjustment_amount
		grand_total_tax += total_tax

	# Sales Grand Total
	append_data(data, 'Grand Total', grand_total_taxable_amount, 
		grand_total_taxable_adjustment_amount, grand_total_tax )
	
	# Blank Line
	append_data(data, '', '', '', '')

	# Purchase Heading
	append_data(data, 'VAT on Purchases', '', '', '')

	grand_total_taxable_amount = 0
	grand_total_taxable_adjustment_amount = 0
	grand_total_tax = 0

	for vat_setting in bahrain_vat_setting.BAHRAIN_vat_purchase_accounts:
		total_taxable_amount, total_taxable_adjustment_amount, \
			total_tax = get_tax_data_for_each_vat_setting(vat_setting, filters, 'Purchase Invoice')
		
		# Adding results to data
		append_data(data, vat_setting.title, total_taxable_amount, 
			total_taxable_adjustment_amount, total_tax)

		grand_total_taxable_amount += total_taxable_amount
		grand_total_taxable_adjustment_amount += total_taxable_adjustment_amount
		grand_total_tax += total_tax

	# Purchase Grand Total
	append_data(data, 'Grand Total', grand_total_taxable_amount, 
		grand_total_taxable_adjustment_amount, grand_total_tax )

	return data

def get_tax_data_for_each_vat_setting(vat_setting, filters, doctype):
	'''
	(BAHRAIN, {filters}, 'Sales Invoice') => 500, 153, 10 \n
	calculates and returns \n
	total_taxable_amount, total_taxable_adjustment_amount, total_tax'''
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')

	# Initiate variables
	total_taxable_amount = 0
	total_taxable_adjustment_amount = 0
	total_tax = 0
	# Fetch All Invoices
	invoices = frappe.get_list(doctype, 
	filters ={
		'docstatus': 1,
		'posting_date': ['between', [from_date, to_date]]
	}, 
	fields =['name', 'is_return'])

	for invoice in invoices:
		invoice_items = frappe.get_list(f'{doctype} Item', 
		filters ={
			'docstatus': 1,
			'parent': invoice.name,
			'item_tax_template': vat_setting.item_tax_template
		}, 
		fields =['item_code', 'net_amount'])

		
		for item in invoice_items:
			# Summing up total taxable amount
			if invoice.is_return == 0:
				total_taxable_amount += item.net_amount
			
			if invoice.is_return == 1:
				total_taxable_adjustment_amount += item.net_amount

			# Summing up total tax
			total_tax += get_tax_amount(item.item_code, vat_setting.account, doctype, invoice.name)
		
	return total_taxable_amount, total_taxable_adjustment_amount, total_tax
		


def append_data(data, title, amount, adjustment_amount, vat_amount):
	"""Returns data with appended value."""
	data.append({"title":title, "amount": amount, "adjustment_amount": adjustment_amount, "vat_amount": vat_amount})

def get_tax_amount(item_code, account_head, doctype, parent):
	if doctype == 'Sales Invoice':
		tax_doctype = 'Sales Taxes and Charges'
	
	elif doctype == 'Purchase Invoice':
		tax_doctype = 'Purchase Taxes and Charges'
	
	item_wise_tax_detail = frappe.get_value(tax_doctype, {
		'docstatus': 1,
		'parent': parent,
		'account_head': account_head
	}, 'item_wise_tax_detail')

	tax_amount = 0
	if item_wise_tax_detail and len(item_wise_tax_detail) > 0:
		item_wise_tax_detail = json.loads(item_wise_tax_detail)
		for key, value in item_wise_tax_detail.items():
			if key == item_code:
				tax_amount = value[1]
				break
	
	return tax_amount