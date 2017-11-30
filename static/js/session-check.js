$( document ).ready(function() {
		var url = "http://10.5.92.201:5000";
		if(!sessionStorage.getItem('username') && !sessionStorage.getItem('token_key')){
			sessionStorage.clear();
	        window.location.href = '/login';
		}else {
			 $( "#nav-username-display" ).html(sessionStorage.getItem('username'));
		}
		var settings = {
		  "async": true,
		  "crossDomain": true,
		  "url": url+"/users/"+sessionStorage.getItem('username'),
		  "method": "GET",
		  "headers": {
		    "accept": "application/json",
		    "authorization": sessionStorage.getItem('token_key'),
		    "cache-control": "no-cache",
		  },
		  error: function (request, message, error) {
		  		sessionStorage.clear();
	            window.location.href = '/login';
	         }
		}

		$.ajax(settings).done(function (response) {
		  console.log(response);
		});
});