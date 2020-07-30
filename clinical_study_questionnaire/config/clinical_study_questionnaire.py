from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Question Master"),
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
					"name": "Question CSQ",
					"description": _("Questions"),
				},
				 {
					"type": "doctype",
					"name": "Answers CSQ",
					"description": _("Anwsers"),
				},
			]
		},
		{
			"label": _("Manage users"),
			"items": [
				{
					"type": "doctype",
					"name": "Interviewer CSQ",
					"description": _("Interviewer"),
				},
				{
					"type": "doctype",
					"name": "Participant CSQ",
					"description": _("Participant"),
				},
			]
		},
	{
			"label": _("Utilities"),
			"items": [
				{
					"type": "page",
					"name": "csq-structure",
					"label": _("Sort Structure"),

					"description": _("Sort Structure"),
				},

			]
		}

	]
