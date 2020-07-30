
//************* Loader Method *******************
frappe.pages['csq-structure'].on_page_load = function (wrapper) {


    let me = this;
    me.page = wrapper.page;
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Manage CSQ Structure',
        single_column: true
    });


    let route = frappe.get_route();
    console.log(route);


    let page_content = $(wrapper).find('.layout-main-section-wrapper');
    //let main_section = me.page.find('.layout-main-section');
    page_content.append('<h1>List of CSQ Structure</h1>');
    page_content.append(frappe.render_template("csq_list"));


    page.wrapper.on("click", ".tester", function () {
        let structure_rows = $(wrapper).find('.structure_rows');
        render_structure(structure_rows);
    });
    //wrapper.pos = new clinical_study_ques
    // tionnaire.csq_structure.render_structure(wrapper);
    //Rightside Menu
    this.page.add_menu_item(__('Build Report'), function () {
        frappe.set_route("List", "Feed", "Report");
    }, 'fa fa-th')


}
// ****** Get Structure from Server *********
render_structure = function (structure_rows) {
    let n_level=get_url_arg("name");
    console.log(get_url_arg("name"));
    // if (n_level.length>2) {
    //     n_level = n_level.split('=');
    //     n_level=n_level[1];
    // }


    frappe.call({
        method: "clinical_study_questionnaire.clinical_study_questionnaire.page.csq_structure.csq_structure.structure_list",
        args:{
          n_level:n_level
        },
        dataType: "json",
        callback: function (r) {
            if (r.message) {
                structure_rows.text("");
                //structure_rows.append(r.message);
                structure_rows.append(frappe.render_template("csq_rows",
                    row_data = r.message
                ));
                var list_row_reference = document.getElementById('list-row-container');
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
    })


};

seethrough_elements = function (list_row_reference) {

    var sort_list = [];
    $(list_row_reference).children().each(function () {
        //console.log($(this).attr("data-idx"));
        sort_list.push($(this).attr("data-idx"));
    });
    console.log(sort_list);

    frappe.call({
        method: "clinical_study_questionnaire.clinical_study_questionnaire.page.csq_structure.csq_structure.update_order",
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