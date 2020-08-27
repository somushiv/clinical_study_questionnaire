import frappe
import json
import datetime

@frappe.whitelist()
def testapi():
    return "Calling from Endpoint"

# ------ Validate Interviewer API ---------- #
@frappe.whitelist()
def interviewer_login():
	#print(frappe.request.data)
	l_object=json.loads(frappe.request.data)

	# This to be Updated Testing with Password
	validate_count = frappe.db.count('Interviewer CSQ', {'interviewer_name': l_object['user']})
	
	if validate_count:
		validate_count=10
		r_Object=frappe.db.get_value('Interviewer CSQ', {'interviewer_name': l_object['user']},['name', 'full_name','interviewer_name','assinged_program','program_name'],as_dict=1)
		r_Object.update({"response":"200","response_message":"Ok"})
		print(r_Object)
	else:
		r_Object={"message":"204","response_message":"Not Found"}

	return (r_Object)

# ------ Registration of the Particpants ------ #
@frappe.whitelist()
def get_participant():
	p_object=json.loads(frappe.request.data)
	db_object={}
	if p_object['participant_id']:
		
		db_object=frappe.db.get_value('Participant CSQ',{'name':p_object['participant_id']},
		['name','participant_name','mobile_number','age','gendar',
		'marital_status','medical_school_year','religion',
		'program_name','assinged_program','registrant__name','registered_by','parent_occupation'],as_dict=1)
	else:
		# Get Interviewer ID Details
		iv_object=frappe.db.get_value('Interviewer CSQ', {'name':p_object['Interviewer_id']},
		['name','full_name','assinged_program','program_name'],as_dict=1)
		db_object={"registrant__name":iv_object['full_name'],
			"registered_by":iv_object['name'],
			"assinged_program":iv_object['assinged_program'],
			"program_name":iv_object['program_name']}
		
	r_object=form_participant(db_object)
	return r_object
	
	
def form_participant(db_object):
	
	f_object={
  "participant_name":{
    "variable_name": "participant_name",
    "label":"Participant Name",
    "data_type": "varchar",
    "value": validate_document(db_object,"participant_name"),
    "user_input":1
  },
  
  "mobile_number":{
    "variable_name": "mobile_number",
    "label":"Mobile Number",
    "data_type": "varchar",
    "value": validate_document(db_object,"mobile_number"),
    "user_input":1
  },
  "email_id":{
    "variable_name": "email_id",
    "label":"Email ID",
    "data_type": "varchar",
    "value": validate_document(db_object,"email_id"),
    "user_input":1
  },
    "password":{
    "variable_name": "password",
    "label":"Password",
    "data_type": "varchar",
    "value": validate_document(db_object,"password"),
    "user_input":1
  },
  "age":{
    "variable_name": "age",
    "label":"Age",
    "data_type": "int",
    "value":validate_document(db_object,"age"),
    "user_input":1
  },
  "gender":{
    "variable_name": "gendar",
    "label":"Gendar",
    "data_type": "select",
    "value": validate_document(db_object,"gendar"),
    "option": [
      "Male",
      "Female",
      "Transgender",
      "Decline to answer",
      "None",
      "Declined to answer"
    ],
    "user_input":1
  },
  "marital_status":{
    "variable_name": "marital_status",
    "label":'Marital Status',
    "data_type": "select",
    "value": validate_document(db_object,"marital_status"),
    "option": [
      "Currently Married",
      "Never Married/Single",
      "Divorced",
      "Separated",
      "Widow/Widower",
      "Deserted",
      "Declined to answer"
    ],
    "user_input":1
  },
  "medical_school_year":{
    "variable_name": "medical_school_year",
    "label":"Medical School Year",
    "data_type": "select",
    "value": validate_document(db_object,"medical_school_year"),
    "option": [
      "First Year MBBS",
      "Second Year MBBS",
      "Third Year MBBS",
      "Fourth Year MBBS",
      "Internship",
      "Declined to answer"
    ],
    "user_input":1
  },
  "religion":{
    "variable_name": "religion",
    "label":"Religion",
    "data_type": "select",
    "value": validate_document(db_object,"religion"),
    "option": [
      "Hindu",
      "Muslim",
      "Sikh",
      "Buddhist",
      "Christian",
      "Jain",
      "Jewish",
      "Paris/ Zoroastrian",
      "None",
      "Declined to answer"
    ],
    "user_input":1
  },
  "parent_occupation":{
    "variable_name": "parent_occupation",
    "label":"Parent Occuption",
    "data_type": "varchar",
    "value": validate_document(db_object,"parent_occupation"),
    "user_input":1
  },
  "language":{
    "variable_name": "language",
    "label":"Language",
    "data_type": "varchar",
    "value": "English",
    "user_input":0
  },
  "participant_type":{
    "variable_name": "participant_type",
    "label":"Participant Type",
    "data_type": "varchar",
    "value": "Medical Student",
    "user_input":0
  },

  
  "program_name":{
    "variable_name": "program_name",
    "label":"Program Name",
    "data_type": "varchar",
    "value": validate_document(db_object,"program_name"),
    "user_input":0
  },
  "assinged_program":{
    "variable_name": "assinged_program",
    "data_type": "varchar",
    "value": validate_document(db_object,"assinged_program"),
    "user_input":0
  },
 
  
  
}
	return f_object

# ---- Validate Field for Value ---------
def validate_document(doc_var,validate_key):	
	if validate_key in doc_var.keys():
		return doc_var[validate_key]
	else:
		return ""

# ------ Particpants Self Registration ----- #
@frappe.whitelist()
def participant_registration():
  # Validate for Unique Email.id and phone number
  l_object = json.loads(frappe.request.data)

  r_validate = frappe.db.count('Participant CSQ',{'mobile_number':  l_object['mobile_number'],'email_id':  l_object['email_id']})
  if r_validate:
    return_object={"message":"204","response_message":"User registred!!!"}
  else:
    doc = frappe.get_doc({
      "doctype": 'Participant CSQ', 
      "participant_name": l_object['participant_name'],
      "mobile_number": l_object['mobile_number'],
      "email_id": l_object['email_id'],
      "password": l_object['password'],
      "language": l_object['language'],
      "age": l_object['age'],
      "gendar": l_object['gendar'],
      "marital_status": l_object['marital_status'],
      "medical_school_year": l_object['medical_school_year'],
      "religion": l_object['religion'],
      "program_name": l_object['program_name'],
      "assinged_program": l_object['assinged_program'],
      "parent_occupation": l_object['parent_occupation']
      })
    doc.insert()
    
    return_object={"message":"200","response_message":"You have registred, You can login now!!!"}


  return return_object



# ------ Validate Interviewer API ---------- #
@frappe.whitelist()
def particpant_login():
  #print(frappe.request.data)
  l_object=json.loads(frappe.request.data)

  # This to be Updated Testing with Password
  validate_count = frappe.db.count('Participant CSQ', {'mobile_number': l_object['mobile_number']})
  if validate_count:
    r_Object = frappe.db.get_value('Participant CSQ', {'mobile_number': l_object['mobile_number']},
                                   ['name', 'participant_name', 'mobile_number', 'medical_school_year', 'program_name',
                                    'assinged_program'], as_dict=1)
  #
    response_stage=validate_response_stage(r_Object['name'])
    r_Object.update(response_stage)
    if response_stage['response_stage']==1:
      ################# Concent Response to be updated

      program_Object = frappe.db.get_value('Programs CSQ', {'name': r_Object['assinged_program']}, ['user_consent'],
                                           as_dict=1)

      r_Object.update(program_Object)

    return_object = r_Object
  else:
    return_object = {"message": "204", "response_message": "Not Found"}






  return return_object

def validate_response_stage(participant_id):
  rs_count =frappe.db.count('Responses CSQ',{'participant_id':participant_id})
  if rs_count==0:
    return {"response_stage": 1, "user_text": "Not Started"}
  elif rs_count==1:
    return {"response_stage": 2, "user_text": "Stage 2"}
  elif rs_count==2:
    return {"response_stage": -2, "user_text": "Completed"}

# ------ Password Change API ---------- #
@frappe.whitelist()
def particpant_passwordchange():
    l_object = json.loads(frappe.request.data)

    # This to be Updated Testing with Password
    r_object = frappe.db.get_value('Participant CSQ', {'mobile_number': l_object['mobile_number']})

    if r_object:

        frappe.db.set_value('Participant CSQ', r_object, 'password', l_object['password'])
        return_object={"response": "200", "response_message": "Ok"}
    else:
        return_object={"response": "200", "response_message": "Not Found"}

    return return_object

@frappe.whitelist()
def particpant_response():
    res_object = json.loads(frappe.request.data)
    # get particpant  Name
    par_object = frappe.db.get_value('Participant CSQ', {'name':res_object['particpant_id']}, ['name', 'participant_name'],as_dict=1)
    pro_object = frappe.db.get_value('Programs CSQ', {'name': res_object['program_id']},['name', 'program_name'],as_dict=1)


    doc = frappe.new_doc('Responses CSQ')
    doc.participant_id = res_object['particpant_id']
    doc.participant_name=par_object['participant_name']
    doc.program_id=res_object['program_id']
    doc.program_name = pro_object['program_name']
    doc.response_stage = res_object['response_stage']
    doc.response_date=datetime.datetime.now()
    doc.insert()

    # ----- Get Inserted Value ----- #
    response_object = frappe.db.get_value('Responses CSQ', {'participant_id': res_object['particpant_id'],'program_id': res_object['program_id']},['name'], as_dict=1)

    # --- Update to Answer Table --
    idx=1
    for answer_row in res_object['answers']:
        ans_doc = frappe.new_doc('Responses Answer CSQ')
        ans_doc.parent = response_object['name']
        ans_doc.parentfield = 'response_answer'
        ans_doc.parenttype ='Responses CSQ'
        ans_doc.idx=idx
        ans_doc.question_id =answer_row['question_id']
        ans_doc.response_answer = answer_row['response_answer']
        ans_doc.insert()

        print(answer_row['question_id'])


    return_object = {"response": "200", "response_message": "Ok"}
    return  response_object
