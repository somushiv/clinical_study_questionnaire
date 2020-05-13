import frappe
import json

@frappe.whitelist()
def testapi():
    return "Calling from Endpoint"


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
  "registrant__name":{
    "variable_name": "registrant__name",
    "label": "Registrant name",
    "data_type": "varchar",
    "value": validate_document(db_object,"registrant__name"),
    "user_input":0
  },
  "registered_by":{
    "variable_name": "registered_by",
    "label":"Registered By",
    "data_type": "varchar",
    "value": validate_document(db_object,"registered_by"),
    "user_input":0
  }
  
}
	return f_object

#Validate Field for Value
def validate_document(doc_var,validate_key):	
	if validate_key in doc_var.keys():
		return doc_var[validate_key]
	else:
		return ""