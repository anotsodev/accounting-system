var url = "http://localhost:5000";
$( document ).ready(function(){

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
	                 get_all(response, url);
	            }
	      }

	  $.ajax(settings);
});
function get_all(response, url){
  var response_text = response;
   records_rows_a = "";
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
            get_cat_name(response, val)
          },
        }
        $.ajax(settings);
   });
}

function get_cat_name(response, val){
    records_rows_a += "<tr>";
    records_rows_a += ("<td>"+val['date']+"</td>");
    records_rows_a += ("<td>"+response['name']+"</td>");
    records_rows_a += ("<td>"+val['description']+"</td>");
    if(response['type'] == 'expense'){
      records_rows_a += ("<td><span style='color: red;'>-"+val['amount']+"</span></td>");
      records_rows_a += ("<td><span class='label label-danger'>"+response['type']+"</span></td>");
    }else{
      records_rows_a += ("<td><span style='color: green;'>+"+val['amount']+"</span></td>");
      records_rows_a += ("<td><span class='label label-success'>"+response['type']+"</span></td>");
    }
    records_rows_a += ("<td><button type='button' class='btn btn-danger btn-sm btn-toastr' data-context='success' data-message='Deleted successfully' data-position='top-right' onclick='delete_record("+ '"'+val['id']+'"' +")'>Remove Record</button>");
    records_rows_a += "</tr>";

    $( "#records-rows-all" ).html(records_rows_a);
}

// function delete_record(rid) {
//   var settings = {
//     "async": true,
//     "crossDomain": true,
//     "url": url+"/records/"+rid,
//     "method": "DELETE",
//     "headers": {
//       "accept": "application/json",
//       "authorization": sessionStorage.getItem('token_key'),
//       "cache-control": "no-cache",
//     },
//     success: function(){
//       window.location.href = '/transactionhistory';
//     }
//   }

//   $.ajax(settings);
// }
