from __future__ import unicode_literals
import frappe

import json


@frappe.whitelist()
def get_data_clinical():
    return "I am from py file"


@frappe.whitelist()
def particpants_list(n_lavel=''):
    n_lavel = frappe.form.get('program_id')
    if not n_lavel:
        n_lavel = 'CSQ0001'

    p_object = frappe.db.get_list('Participant CSQ', filters={
                                'assinged_program': n_lavel
                                },
                                  fields=['name', 'participant_name', 'gendar', 'medical_school_year'],as_list=True)

    p_list_object=[]
    for p_row in p_object:
        rs_indicator=responses_status(p_row)

        tmp=list(p_row)
        for rs_in in rs_indicator:
            tmp.append(rs_in)
        p_list_object.append(tmp)

    #print(p_object)

    return p_list_object

def responses_status(p_row):
    indicator_list =['<span class="indicator red ellipsis">Pending</span>',
                     '<span class="indicator red ellipsis">Pending</span>',
                        '<span class="indicator red ellipsis">Pending</span>']

    rs_object=frappe.db.get_list('Responses CSQ', filters={
        'participant_id':p_row[0]
    }, fields=['name', 'participant_id', 'response_stage'])
    for rs_row in rs_object:
        ref_value=rs_row['response_stage']-1
        update_text=indicator_list[ref_value]
        update_text=update_text.replace('red','green')
        update_text = update_text.replace('Pending', 'Complete')
        indicator_list[ref_value]=update_text



    return indicator_list



