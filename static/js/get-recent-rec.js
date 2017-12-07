$(document).ready(function(){
	var settings = {
	    "async": true,
	    "crossDomain": true,
	    "url": url+"/records",
	    "method": "GET",
	    "headers": {
	      "authorization": sessionStorage.getItem('token_key'),
	      "cache-control": "no-cache",
	    },
	    success: function (response) {
	                 output_records(response,url);
	            }
	      }

	  $.ajax(settings);
});

function output_records(response,url){
   var response_text = response;
   records_rows = "";
   var count = 0;
   $.each(response_text, function(i, val){

      var settings = {
          "async": true,
          "crossDomain": true,
          "url": url+"/categories/"+val['category_id'],
          "method": "GET",
          "headers": {
            "accept": "application/json",
            "authorization": sessionStorage.getItem('token_key'),
            "cache-control": "no-cache"
          },
          success: function (response) {
            get_category_name(response, val)
          },
        }
        $.ajax(settings);
      count += 1;
      if(count == 10){
        return false;
      }
   });
   
}

function get_category_name(response, val){
    records_rows += "<tr>";
    records_rows += ("<td>"+val['date']+"</td>");
    records_rows += ("<td>"+response['name']+"</td>");
    records_rows += ("<td>"+val['description']+"</td>");
    if(response['type'] == 'expense'){
      records_rows += ("<td><span style='color: red;'>-"+val['amount']+"</span></td>");
      records_rows += ("<td><span class='label label-danger'>"+response['type']+"</span></td>");
    }else{
      records_rows += ("<td><span style='color: green;'>+"+val['amount']+"</span></td>");
      records_rows += ("<td><span class='label label-success'>"+response['type']+"</span></td>");
    }
    records_rows += "</tr>";

    $( "#records-rows" ).html(records_rows);
}