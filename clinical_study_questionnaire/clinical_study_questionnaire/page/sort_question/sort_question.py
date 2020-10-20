from __future__ import unicode_literals
import frappe
import json

@frappe.whitelist()
def get_structure_list(structure_key='CSQ-ST0001'):
    structure_list=frappe.db.get_list('Structure CSQ',
                                      filters={
                                          'parent_structure_csq':structure_key
                                      },
                                      fields=['name', 'title', 'is_group', 'quesiton_code'],
                                      order_by='display_order')

    # This is one child Hardcoded
    x=0
    for  structure_data in structure_list:
        if structure_data['is_group']:
            childrenList = frappe.db.get_list('Structure CSQ',
                                                filters={
                                                    'parent_structure_csq': structure_data['name']
                                                },
                                                fields=['name', 'title', 'is_group', 'quesiton_code'],
                                                order_by='display_order')
            structure_list[x]["children_list"]=childrenList
        x=x=1

    return structure_list

@frappe.whitelist()
def get_question_list(n_lavel=''):
    n_lavel = frappe.form.get('n_level')
    print(n_lavel)
    if not n_lavel:
        n_lavel = 'CSQ-ST0003'

    question_list=frappe.db.get_list('Question CSQ',
                                      filters={
                                          'section_name':n_lavel
                                      },
                                      fields=['name', 'question', 'section_name', 'display_order'],
                                      order_by='display_order')


    return question_list

@frappe.whitelist()
def update_order(sort_list='x'):
    l_objects =json.loads(sort_list)
    for index, l_name in enumerate(l_objects):
        print("========= Output =====", l_name, index)
        frappe.db.set_value('Question CSQ',l_name,
                            {'display_order':index})
    return l_objects