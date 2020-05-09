from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Clinical Study Questionnaire"),
			"items": [
				{
					"type": "doctype",
					"name": "Programs CSQ",
					"description": _("Programs"),
					
				},
				{
					"type": "doctype",
					"name": "Study Desing CSQ",
					"description": _("Study Design"),
				},
				{
					"type": "doctype",
					"name": "Structure CSQ",
					"description": _("Structure"),
				},
				{
					"type": "doctype",
					"name": "Participant CSQ",
					"description": _("Participant"),
				},				 
				 {
					"type": "doctype",
					"name": "Question CSQ",
					"description": _("Questions"),
				},
				 {
					"type": "doctype",
					"name": "Answers CSQ",
					"description": _("Anwsers"),
				},
			]
		}]
