$( document ).ready(function() {
  var url = "http://10.5.92.201:5000"
  // check session
    /*
      Register Section
    */ 
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
              fields_error_handler(request.responseText);
            }
          }
            $.ajax(settings);
    });
    /*
      Register Section End
    */
    // Login Section
    $( "#login" ).click(function() {
      var data = JSON.stringify($('form').serializeObject());
      var response = {};
      var auth
      parsed_data = JSON.parse(data)
      var credential = parsed_data['username']+":"+parsed_data['password'];
      auth = encode_base64(credential)
      var settings = {
            "async": true,
            "crossDomain": true,
            "url": url+"/users/login",
            "method": "POST",
            "headers": {
              "accept": "application/json",
              "content-type": "application/json",
              "cache-control": "no-cache",
              "authorization": auth
            },
            "dataType": "json",
            success: function (response) {
                sessionStorage.setItem('token_key', response['token']);
                sessionStorage.setItem('username', parsed_data['username']);
                window.location.href = '/dashboard';
            },
            error: function (request, message, error) {
              error_message_handler(request.responseText);
            }
          }
            $.ajax(settings);
    }); 

    // Logout
    $( "#logout-account" ).click(function() {
      var settings = {
            "async": true,
            "crossDomain": true,
            "url": url+"/users/logout",
            "method": "POST",
            "headers": {
              "accept": "application/json",
              "authorization": sessionStorage.getItem('token_key')
            }
          }
            $.ajax(settings);
      sessionStorage.clear();
    }); 

    // Add new category
    $( "#add-new-category" ).click(function() {
      var data = JSON.stringify($('form').serializeObject());
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
                error_message_handler(request.responseText);
              }
          }
      $.ajax(settings);
    });

});

function encode_base64(string) {
  // Create Base64 Object
      var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9+/=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/rn/g,"n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}}

      // Encode the String
      var encodedString = Base64.encode(string);
      return encodedString
}

function error_message_handler(error_message){
  $( "#error-message" ).html(JSON.parse(error_message)['message']);
}

function fields_error_handler(error_message){
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

