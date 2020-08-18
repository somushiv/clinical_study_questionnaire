

frappe.pages['csq-response-view'].on_page_load = function(wrapper) {


	program_details();



	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Dristi Responses",
		single_column: true
	});


	let page_content = $(wrapper).find('.layout-main-section-wrapper');
	 page_content.append(frappe.render_template("csq_response_list"));
	 response_make();

}

function program_details(program_id='CSQ0001'){

	// multiple values
let program_object=new frappe.db.get_value('Programs CSQ', program_id, ['name', 'program_name'])
    .then(r => {
        let values = r.message;
        // console.log(values.name, values.program_name)
		set_program_object(values)
    })

}

function set_program_object(values){
	program_object=values;
	console.log(program_object.program_name)
}

function response_make(){
	const assets = [
			"/assets/frappe/css/frappe-datatable.css",
			"/assets/frappe/js/lib/clusterize.min.js",
			"/assets/frappe/js/lib/Sortable.min.js",
			"/assets/frappe/js/lib/frappe-datatable.js"
		];

		frappe.require(assets, () => {
			
			load_particpant_data();
		});
}
function load_particpant_data(){
	  frappe.call({
        method: "clinical_study_questionnaire.clinical_study_questionnaire.page.csq_response_view.csq_response.particpants_list",
        args:{
          n_level:'CSQ0001'
        },
        dataType: "json",
        callback: function (r) {
            if (r.message) {
           		create_datatable(r.message);
            }
        }
    })
}

function create_datatable(p_data) {

	var datatable = new DataTable('.particpants-table', {
			columns: ['P.Ref.Num', 'Full Name', 'Gender', 'Medical School Year','Baseline','Intervention','Assessment'],
			data: p_data,
			layout:'fluid'


		},


);

patchrowwidth();
}
function patchrowwidth(){

	let tmpArray=Array();
	$('.data-table-header thead td').each(function() {
    	tdWidth = $(this).width();
    	tmpArray.push(tdWidth);
		$(this).width("100%");
	});
	console.log(tmpArray);
	$('tbody tr').each(function() {
    	let rowReference = $(this)

	let 	x=0;
    	rowReference.find('td').each(function() {
	//
    		$(this).width(tmpArray[x]+'px !important');
    		x++;
	//
	});

	});
}