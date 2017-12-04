 $( document ).ready(function() {
        var url = "http://localhost:5000"
        $( "#register" ).click(function() {

        var data = JSON.stringify($('form').serializeObject());
        var response = {};

        var settings = {
              "async": true,
              "crossDomain": true,
              "url": url+"/users",
              "method": "POST",
              "headers": {
                "accept": "application/json",
                "content-type": "application/json",
                "cache-control": "no-cache",
              },
              "dataType": "json",
              "data": data,
              success: function () {
                  window.location.href = '/login';
              },
              error: function (request, message, error) {
                handler_err(request.responseText);
              }
            }
              $.ajax(settings);
        });
      });
      function handler_err(error_message){
        $( "#error-message" ).html(function(){
          var ret = "<p>Please check the following fields:</p>"
          error_data = JSON.parse(error_message);
          $.each(error_data["invalid_fields"],function(i, val){
              $.each(val,function(key,val){
                if (key == "field") {
                    ret += "<b>";
                    ret += (val);
                    ret += "</b>";
                }else {
                  ret += "<p>";
                  ret += (val);
                  ret += "</p>";
                }
                
              })
          });
          return ret
        });
      }
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