import frappe
from frappe.utils import cint
from erpnext.manufacturing.doctype.production_order.production_order import add_timesheet_detail
from erpnext.patches.v7_0.convert_timelog_to_timesheet import get_timelog_data

def execute():
	for tlb in frappe.get_all('Time Log Batch', fields=["*"], 
		filters = [["docstatus", "<", "2"]]):
		time_sheet = frappe.new_doc('Timesheet')
		time_sheet.employee= ""
		time_sheet.company = frappe.db.get_single_value('Global Defaults', 'default_company')
		time_sheet.sales_invoice = tlb.sales_invoice

		for data in frappe.get_all('Time Log Batch Detail', fields=["*"],
			filters = {'parent': tlb.name}):
			args = get_timesheet_data(data)
			add_timesheet_detail(time_sheet, args)

		time_sheet.docstatus = tlb.docstatus
		time_sheet.save(ignore_permissions=True)

def get_timesheet_data(data):
	time_log = frappe.get_all('Time Log', fields=["*"],
		filters = {'name': data.time_log})[0]

	return get_timelog_data(time_log)