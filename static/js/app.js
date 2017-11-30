$( document ).ready(function() {
    
    $( "#register" ).click(function() {
      var url = "http://10.5.92.201:5000"

      var data = JSON.stringify($('form').serializeObject())

      console.log(data)

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
            success: function (data) {
                window.location.href = '/login';
            },
            error: function (request, message, error) {
              console.log(message)
            }
          }
            $.ajax(settings);
    });

});



$.fn.serializeObject = function()
{
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

