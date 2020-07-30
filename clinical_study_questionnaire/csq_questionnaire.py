import frappe
import json
import sys

@frappe.whitelist()
def test_api():
    return "Calling from Endpoint"


# ------ Validate Interviewer API ---------- #
@frappe.whitelist()
def study_design():
    # print(frappe.request.data)

    r_study_desing = [{"key_id": "CD001", "label": "Baseline Assement", "comment": "Post Registration"},
                      {"key_id": "CD002", "label": "Intervention", "comment": "Post Registration"},
                      {"key_id": "CD003", "label": "Week Assessment", "comment": "After 1 week"}]
    return (r_study_desing)


@frappe.whitelist()
def get_csq_questions(var_section_name='', title_dist=''):
    # q_object = frappe.db.get_list('Question CSQ',{'section_name':['IN','CSQ-ST0003','CSQ-ST0002']},
    # ['section_title','name','question',  'upload_image'])
    # q_object = frappe.db.sql(
    #     "select section_title,name,question,upload_image from `tabQuestion CSQ` where section_name in ('CSQ-ST0003','CSQ-ST0004','CSQ-ST0005') order by section_name",
    #     as_dict=1);
    q_object=frappe.db.get_list('Question CSQ',
                                              filters={
                                                  'section_name': var_section_name
                                              },
                                              fields=['name', 'section_title', 'question',
                                                      'upload_image', 'upload_video'],
                                              order_by='name',
                                              )
    #print(len(q_object))
    x = 0
    for q_row in q_object:
        # -- Get Answers --
        q_row=validate_none(q_row)
        a_object = frappe.db.get_list('Answers CSQ', {'parent': q_row['name']}, ['answer_text', 'score'])
        answer_object = {"answer": a_object}
        q_object[x].update(answer_object)

        #update Title
        q_object[x].update({'page_titles':title_dist})

       # print(q_object[x])
        x += 1

    if len(q_object)>0:
        q_object=q_object[0]
    return q_object

def validate_none(q_row):
    for f_key, f_value in q_row.items():

        if f_value is None:
            q_row[f_key]='None'
    return q_row


# ------ Program with Settings ------ #

def get_program_settings(program_reference):
    q_object = frappe.db.get_value('Settings CSQ',
                                   {
                                       'program_reference': program_reference
                                   },
                                   ['title', 'setting_value'], as_dict=1)
    return q_object


def get_single_question(question_code):
    q_object =frappe.db.get_value('Question CSQ',
                                  {'question_code':question_code},
                                  ['name', 'question', 'section_name', 'section_title', 'has_video', 'upload_video', 'has_image', 'upload_image', 'question_type'],
                                  as_dict=1
                                  )
    return q_object




def get_questions():
    question_reference = get_program_settings('CSQ0001')
    q_list = question_reference['setting_value'].split(",")

    for q_element in q_list:
        question = get_single_question(q_element.replace(" ", ""))
        print(question)


# def get_structure1():
#     s_list=json.loads('{"CSQ-ST0001":["CSQ-ST0017",{"CSQ-ST0002":["CSQ-ST0003","CSQ-ST0004","CSQ-ST0005","CSQ-ST0006","CSQ-ST0007","CSQ-ST00018","CSQ-ST0008","CSQ-ST0009","CSQ-ST0010"]},"CSQ-ST0012","CSQ-ST0013","CSQ-ST0014","CSQ-ST0015","CSQ-ST0016"]}')
#     loopelement((s_list))
#
# def loopelement(j_object, prefix=''):
#
#     if type(j_object) is dict:
#         for (key,value) in j_object.items():
#             print(prefix, key)
#             if len(value)>0:
#                 prefix = prefix + "-" + key
#                 loopelement(value, prefix)
#             else:
#                 print('-',value)
#     elif type(j_object) is list:
#         for key in j_object:
#             if type(key) is dict:
#
#                 loopelement(key,prefix)
#             else:
#                 print( prefix, '-- Calling Database', key)

@frappe.whitelist()
def questions():
    return_questions=get_structure()
    #print(return_questions)
    return return_questions

def get_structure(var_name='CSQ-ST0001', title_counter=1, title_dist={'h1': '', 'h2': '', 'h3': ''},question_list=[]):


    structure_object = frappe.db.get_list('Structure CSQ',
                                              filters={
                                                  'parent_structure_csq': var_name
                                              },
                                              fields=['name', 'title', 'display_order', 'parent_structure_csq'],
                                              order_by='display_order',
                                              )

    for s_row in structure_object:
        #print(s_row)
        siblings=validate_siblings(s_row['name'])
        if title_counter==1:
            title_dist = {'h1': '', 'h2': '', 'h3': ''}

        title_dist['h'+str(title_counter)]=s_row['title']
        #print(title_dist)
        if siblings:
            get_structure(s_row['name'], title_counter+1,title_dist,question_list)
        else:
            pass
           # print('***** title *****', title_dist)
        question_list.append(get_csq_questions(s_row['name'], title_dist))

    return question_list


def validate_siblings(var_name=''):
    q_object=frappe.db.get_list('Structure CSQ',
                                              filters={
                                                  'parent_structure_csq': var_name
                                              },
                                              fields=['name', 'title', 'display_order', 'parent_structure_csq'],
                                              order_by='display_order',
                                              )
    if len(q_object)==0:
        return 0
    else:
        return 1
