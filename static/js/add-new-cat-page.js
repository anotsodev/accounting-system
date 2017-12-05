$(document).ready(function(){
	var url = "http://10.5.92.201:5000";
	$( "#add-new-category" ).click(function() {
      var data = JSON.stringify($('#new-cat-form').serializeObject());
      var settings = {
        "async": true,
        "crossDomain": true,
        "url": url+"/categories",
        "method": "POST",
        "headers": {
          "accept": "application/json",
          "content-type": "application/json",
          "authorization": sessionStorage.getItem('token_key'),
          "cache-control": "no-cache"
          },
          "data": data,
          success: function (response) {
                  window.location.href = '/categorylist';
            },
          error: function (request, message, error) {
                inv_handler(request.responseText,"add-new-category");
              }
          }
      $.ajax(settings);
    });
});

$.fn.serializeObject = function() {
          var o = {};
          var a = this.serializeArray();
          $.each(a, function() {
              if (o[this.name] !== undefined) {
                  if (!o[this.name].push) {
                      o[this.name] = [o[this.name]];
                  }
                  o[this.name].push(this.value || '');
              } else {
                  o[this.name] = this.value || '';
              }
          });
          return o;
      };

function inv_handler(error_message,id){
  // console.log(JSON.parse(error_message)['message']);
  if(JSON.parse(error_message)['message'] == undefined){
    $( "#error-message"+"-"+id ).html("<b>Type is a required field</b>");
  }else {
    $( "#error-message"+"-"+id ).html("<b>"+JSON.parse(error_message)['message']+"</b>");
  }
  
}