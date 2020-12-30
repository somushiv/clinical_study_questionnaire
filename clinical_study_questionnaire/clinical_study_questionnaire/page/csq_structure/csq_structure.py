from __future__ import unicode_literals
import frappe
import json


@frappe.whitelist()
def get_data_clinical():
    return "I am from py file"

@frappe.whitelist()
def structure_list(n_lavel=''):
    n_lavel = frappe.form.get('n_level')
    if not n_lavel:
        #Patch for dynamic top
        structure_data = frappe.db.get_value('Structure CSQ', {'title' : 'Start'}, ['name'], as_dict=1)
        
        n_lavel = structure_data["name"]

    # Get Root Node which has value left =1
    # root_keyobject=frappe.db.get_list('Structure CSQ',
    #                                filters ={
    #                                    'is_group':1,
    #                                    'lft':1
    #                                })
    # root_keyobject=root_keyobject[0]

    structure_list = get_structure_list(n_lavel)

    return structure_list

def get_structure_list(structure_key=''):
    structure_list=frappe.db.get_list('Structure CSQ',
                                      filters={
                                          'parent_structure_csq':structure_key
                                      },
                                      fields=['name', 'title', 'is_group', 'quesiton_code'],
                                      order_by='display_order')
    return structure_list

@frappe.whitelist()
def update_order(sort_list='x'):
    l_objects =json.loads(sort_list)
    for index, l_name in enumerate(l_objects):
        print("========= Output =====", l_name, index)
        frappe.db.set_value('Structure CSQ',l_name,
                            {'display_order':index})
    return l_objects