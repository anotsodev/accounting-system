$(document).ready(function(){
	var url = "http://10.5.92.201:5000";
	$( "#add-new-trans" ).click(function() {
	      var data = JSON.stringify($('#new-trans-form').serializeObject());
	      var settings = {
	        "async": true,
	        "crossDomain": true,
	        "url": url+"/records",
	        "method": "POST",
	        "headers": {
	          "accept": "application/json",
	          "content-type": "application/json",
	          "authorization": sessionStorage.getItem('token_key'),
	          "cache-control": "no-cache"
	        },
	        "processData": false,
	        "data": data,
	        success: function (response) {
	           window.location.href = '/dashboard';
	        },
	        error: function (request, message, error) {
	            inv_handler(request.responseText,"add-new-trans");
	          }
	      }
	        $.ajax(settings);
	    }); 
	var settings = {
          "async": true,
          "crossDomain": true,
          "url": url+"/categories",
          "method": "GET",
          "headers": {
            "authorization": sessionStorage.getItem('token_key'),
            "cache-control": "no-cache",
          },
          success: function (response) {
                       dropdown_cat(response)
                  }
            }

        $.ajax(settings);
});

function inv_handler(error_message,id){
    err = JSON.parse(error_message);
    $( "#error-message"+"-"+id ).html("<b>"+err['message']+"</b>");
}
function dropdown_cat(response){
    var out = "";

    var response_text = JSON.parse(response);
    out += "<option value='' selected>Choose Category</option>";
    out += "<optgroup label='Income'>";
    $.each(response_text, function(i, val){
      if(val['type'] == 'income'){
        out += "<option value="+val['id']+">";
        out += val['name']
        out += "</option>";
      }
    }); 
    out += "</optgroup>";

    out += "<optgroup label='Expense'>";
    $.each(response_text, function(i, val){
      if(val['type'] == 'expense'){
        out += "<option value="+val['id']+">";
        out += val['name']
        out += "</option>";
      }
    }); 
    out += "</optgroup>";
    $( "#category-picker" ).html(out);

}
