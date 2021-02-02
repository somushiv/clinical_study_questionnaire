import frappe
import json
import sys
from frappe.utils import get_url

@frappe.whitelist()
def test_api():
    return "Calling from Endpoint"


# ------ Validate Interviewer API ---------- #
@frappe.whitelist()
def study_design():

    # print(frappe.request.data)
    l_object = json.loads(frappe.request.data)
    particpant_id = l_object['particpant_id']


    #For Intervention only
    particpant_object = frappe.db.get_value('Participant CSQ', {'name': particpant_id},['name','assinged_program'],as_dict=1)
    print(particpant_object)


    q_object = frappe.db.get_list('Study Desing CSQ', filters={'strudy_program': 'CSQ0001'},
                                  fields=['name', 'title', 'study_order'],
                                  order_by='study_order')

    # Validate logged in Particpant status
    response_satus = validate_response_stage(particpant_id)
     
    if response_satus >= 0:
        
        x = 0
        for q_row in q_object:
            menu_object = {"status": 0, 'response_stage': 0}
            if response_satus > -2:
                vCheck = response_satus + 1;
                if q_row['study_order'] == vCheck:
                    menu_object = {"status": 1, 'response_stage': q_row['study_order']}
                    print(menu_object)
            q_object[x].update(menu_object)
            x = x + 1

        if (particpant_object['assinged_program']=='CSQ0003'):
            q_object[1]['status']=1
            del q_object[0]
            del q_object[1]
            q_object[0]["response_stage"]=2
            print(q_object)


    else:
        q_object = [{
            "name": "Nothing",
            "title": "Thank you for Completing questionnaire",
            "study_order": 0,
            "status": -1,
            "response_stage": 0
        }]





    return (q_object)


def validate_response_stage(participant_id='NS00002'):
    part_object = frappe.db.get_list('Responses CSQ', {'participant_id': participant_id},
                                  group_by='response_stage')
    rs_count=len(part_object)

    if rs_count == 0:
        return 0
    elif rs_count == 1:
        return 1
    elif rs_count == 2:
        return 2
    elif rs_count == 3:
        return -1


def get_csq_questions(var_section_name='', title_dist='',user_description=''):
    # q_object = frappe.db.get_list('Question CSQ',{'section_name':['IN','CSQ-ST0003','CSQ-ST0002']},
    # ['section_title','name','question',  'upload_image'])
    # q_object = frappe.db.sql(
    #     "select section_title,name,question,upload_image from `tabQuestion CSQ` where section_name in ('CSQ-ST0003','CSQ-ST0004','CSQ-ST0005') order by section_name",
    #     as_dict=1);
    q_object = frappe.db.get_list('Question CSQ',
                                  filters={
                                      'section_name': var_section_name
                                  },
                                  fields=['name', 'section_title', 'question',
                                          'upload_image', 'upload_video','question_type','section_name'],
                                  order_by='display_order',
                                  )

    x = 0
    
    for q_row in q_object:
        # -- Get Answers --
        q_row = validate_none(q_row)
        title_object1=generate_header(q_row['section_name'],[])
        

        a_object = frappe.db.get_list('Answers CSQ', {'parent': q_row['name']}, ['answer_text', 'score', 'branch_question', 'text_input'])

        xy=0
        for a_obj in a_object:

            if a_obj['branch_question'] is None:

                a_object[xy]['branch_question']="0"

            if a_obj['text_input'] is None:
                a_object[xy]['text_input'] = 0
            elif a_obj['text_input'] == 'No':
                a_object[xy]['text_input'] = 0
            elif a_obj['text_input'] == 'Yes':
                a_object[xy]['text_input'] = 1
            xy=xy+1


        # print("============",a_object)
        if not a_object:
            a_object.append({"answer_text": "","score": "","branch_question": "","text_input": 0})
        answer_object = {"answer": a_object}

        q_object[x].user_description=user_description
        q_object[x].update(answer_object)

        # update Title
       
        q_object[x].update({'page_titles': title_object1})

        x += 1

    if len(q_object) == 1:
        q_object = q_object[0]

    return q_object


def validate_none(q_row):
    for f_key, f_value in q_row.items():

        if f_value is None:
            q_row[f_key] = 'None'
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
    q_object = frappe.db.get_value('Question CSQ',
                                   {'question_code': question_code},
                                   ['name', 'question', 'section_name', 'section_title', 'has_video', 'upload_video',
                                    'has_image', 'upload_image', 'question_type'],
                                   as_dict=1
                                   )
    return q_object


def get_questions():
    question_reference = get_program_settings('CSQ0001')
    q_list = question_reference['setting_value'].split(",")

    for q_element in q_list:
        question = get_single_question(q_element.replace(" ", ""))
    # print(question)


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

def interaction_module():
    structure_object = frappe.db.get_list('CSQ Intervention',
                                          fields=['name', 'intervention_title', 'intervention_description',
                                                  'media_type', 'media','youtube_link'],
                                          order_by='name')
    idx=0
    for structure_row in structure_object:
        print(structure_row['name'])
        if structure_row['media_type']!="Youtube":
            structure_object[idx]["media"]=get_url()+structure_row['media']
        else:
            structure_object[idx]["media"] =  structure_row['youtube_link']
        idx=idx+1



    print(frappe.local.request.host)
    site_name =get_url()
    print(site_name)
    print(structure_object)
    return structure_object


def get_starting_id():
    #Patch for dynamic top
    structure_data = frappe.db.get_value('Structure CSQ', {'title' : 'Start'}, ['name'], as_dict=1)

    n_lavel = structure_data["name"]
    return n_lavel


@frappe.whitelist()
def questions():
    l_object = json.loads(frappe.request.data)
    response_stage = l_object['response_stage']

    if type(response_stage)==str:
        response_stage=int(response_stage)
    print("response_stage ", response_stage)
    question_mode=1
    if response_stage == 2:
        return_questions = interaction_module()
        question_mode=2
        returnObject = {'question_mode': question_mode, 'interaction_questions': return_questions}
    else:
        
        starting_code=get_starting_id()
        return_questions = get_structure(starting_code, 1, {'h1': '', 'h2': '', 'h3': ''}, [])
        returnObject = {'question_mode': question_mode, 'questions': return_questions}
    # print(return_questions)

    return returnObject

def generate_header(structure_id='CSQ-ST0015',header_list=[]):
   
    structure_data = frappe.db.get_value('Structure CSQ', {'title' : 'Start'}, ['name'], as_dict=1)

    n_lavel = structure_data["name"]
    structure_object = frappe.db.get_value('Structure CSQ',{'name': structure_id},['name', 'title', 'display_order', 'parent_structure_csq'],as_dict=1)
      
    if n_lavel!=structure_object['parent_structure_csq']:
        print("not empty")
        
        header_list=generate_header(structure_object['parent_structure_csq'],header_list)       
    
    header_list.append(structure_object['title'])    
    # print(header_list)
    return header_list
        

                    


def get_structure(var_name, title_counter, title_dist, question_list):
    structure_object = frappe.db.get_list('Structure CSQ',
                                          filters={
                                              'parent_structure_csq': var_name
                                          },
                                          fields=['name', 'title', 'display_order', 'parent_structure_csq','description'],
                                          order_by='display_order',
                                          )

    siblings = validate_siblings(var_name)
    if title_counter == 1:
        title_dist = {'h1': '', 'h2': '', 'h3': ''}

    for s_row in structure_object:
        # print(s_row)
        siblings = validate_siblings(s_row['name'])
        if title_counter == 1:
            title_dist = {'h1': '', 'h2': '', 'h3': ''}

        title_dist['h' + str(title_counter)] = s_row['title']
        # print(title_dist)
        if siblings:
            print("**********","Hello there")
            get_structure(s_row['name'], title_counter + 1, title_dist, question_list)
        else:
            pass
        # print('***** title *****', title_dist)
       
        question_return = get_csq_questions(s_row['name'], title_dist,s_row['description'])
        if type(question_return) is list:
            for q_return_row in question_return:
                question_list.append(q_return_row)

    return question_list


def validate_siblings(var_name=''):
    q_object = frappe.db.get_list('Structure CSQ',
                                  filters={
                                      'parent_structure_csq': var_name
                                  },
                                  fields=['name', 'title', 'display_order', 'parent_structure_csq'],
                                  order_by='display_order',
                                  )
    if len(q_object) == 0:
        return 0
    else:
        return 1
