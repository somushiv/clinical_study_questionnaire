frappe.pages['sort-question'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Sort Question',
		single_column: true
	});
	 let page_content = $(wrapper).find('.layout-main-section-wrapper');
	 page_content.append(frappe.render_template("csq_list"));
	generate_data(page);
page.add_action_icon(__("fa fa-home"), function() {

		frappe.set_route('#modules/Clinical Study Questionnaire');
	});
}

async function generate_data(page){
	let page_content = page.wrapper.find('.layout-main-section');
    await frappe.call({
        method: "clinical_study_questionnaire.clinical_study_questionnaire.page.sort_question.sort_question.get_structure_list",

        dataType: "json",
        callback: function (r) {
            if (r.message) {

                 let structure_template=frappe.render_template("strucutre_list",
				structure_data=r.message);

                 $(".structure-data-list").html(structure_template);
					$(".get-answers").click(function(){
						var refthis=$(this)
						console.log("id ",refthis.attr("dataref"));
						getquesitons(refthis.attr("dataref"),refthis.text());
					});

                }
            }
        }
    )
}

async  function getquesitons(structure_id='',title_text){

	    await frappe.call({
        method: "clinical_study_questionnaire.clinical_study_questionnaire.page.sort_question.sort_question.get_question_list",
            args:{
          n_level:structure_id
        },
        dataType: "json",
        callback: function (r) {
            if (r.message) {



                let question_data=frappe.render_template("question_list",
				row_data=r.message);

                 $(".question-data-list").html(question_data);
                  $(".structure-title-reference").html(title_text);
                 var list_row_reference = document.getElementById('question-data-list');

                new Sortable(list_row_reference, {
                    animation: 150,
                    ghostClass: 'blue-background-class',
                    onEnd: function (evt) {
                        var itemEl = evt.item;  // dragged HTMLElement
                        seethrough_elements(list_row_reference);

                    }
                });

                }
            }
        }
    )
}


seethrough_elements = function (list_row_reference) {

    var sort_list = [];
    $(list_row_reference).children().each(function () {
        //console.log($(this).attr("data-idx"));
        sort_list.push($(this).attr("data-idx"));
    });
    console.log(sort_list);

    frappe.call({
        method: "clinical_study_questionnaire.clinical_study_questionnaire.page.sort_question.sort_question.update_order",
        dataType: "json",
        args: {
            sort_list: JSON.stringify(sort_list),
        },

        callback: function (r) {
            if (r.message) {
                console.log("from Server", r.message);
            }
        }
    });

}