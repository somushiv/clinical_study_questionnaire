import frappe
import json

@frappe.whitelist()
def testapi():
    return "Calling from Endpoint"

# ------ Validate Interviewer API ---------- #
@frappe.whitelist()
def study_desing():
	#print(frappe.request.data)
	
    r_study_desing=[{"key_id":"CD001","label":"Baseline Assement","comment":"Post Registration"}, 
            {"key_id":"CD002","label":"Intervention","comment":"Post Registration"},
            {"key_id":"CD003","label":"Week Assessment","comment":"After 1 week"}]
    return (r_study_desing)

@frappe.whitelist()
def questions():

    #q_object = frappe.db.get_list('Question CSQ',{'section_name':['IN','CSQ-ST0003','CSQ-ST0002']},['section_title','name','question',  'upload_image'])
    q_object=frappe.db.sql("select section_title,name,question,upload_image from `tabQuestion CSQ` where section_name in ('CSQ-ST0003','CSQ-ST0004','CSQ-ST0005') order by section_name",as_dict=1);
    print(len(q_object))
    x=0
    for q_row in q_object:
        # -- Get Answers --
        a_object = frappe.db.get_list('Answers CSQ',{'parent':q_row['name']},['answer_text','score'])
        print(q_row['name'])
        answer_object = {"answer":a_object}
        q_object[x].update(answer_object)
        print(q_object[x])
        x +=1

    return q_object
