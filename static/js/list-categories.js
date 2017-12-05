$(document).ready(function(){
	var url = "http://10.5.92.201:5000";
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
                   output_cat(response);
              }
        }

    $.ajax(settings);
});
function output_cat(response){
  var income_body = "";
  var expense_body = "";
  var income_trans_count = 0;
  var expense_trans_count = 0;
  var response_text = JSON.parse(response);
  $.each(response_text, function(i, val){
    income_body += "<tr>";
    expense_body += "<tr>";
    if(val['type'] == 'income'){
      income_body += ("<td>"+val['name']+"</td>");
      income_body += ("<td>0 Transactions</td>");
      income_body += ("<td><button type='button' class='btn btn-danger' disabled>Delete</button></td>");
    }else{
      expense_body += ("<td>"+val['name']+"</td>");
      expense_body += ("<td>0 Transactions</td>");
      expense_body += ("<td><button type='button' class='btn btn-danger' disabled>Delete</button></td>");
    }
    income_body += "</tr>";
    expense_body += "</tr>";
  }); 
  $( "#income-table" ).html(income_body);
  $( "#expense-table" ).html(expense_body);

}