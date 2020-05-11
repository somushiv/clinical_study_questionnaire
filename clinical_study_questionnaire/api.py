import frappe

@frappe.whitelist()
def testapi():
    return "Clinical Test Api"
