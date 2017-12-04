$(document).ready(function(){
  var url = "http://localhost:5000";
  var settings = {
      "async": true,
      "crossDomain": true,
      "url": url+"/users/"+sessionStorage.getItem('username'),
      "method": "GET",
      "headers": {
        "accept": "application/json",
        "authorization": sessionStorage.getItem('token_key'),
        "cache-control": "no-cache"
      },
      success: function (response) {
        output_balance(response);
      }
    }

    $.ajax(settings);
});

function output_balance(response) {
  var response_text = JSON.parse(response);
  $( "#user-balance" ).html('<h4 class="card-title">PHP '+parseFloat(response_text['balance'])+'</h4>');
}