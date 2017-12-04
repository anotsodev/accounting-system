$( document ).ready(function() {
		// for dashboard only
		// var url = "http://10.5.92.201:5000";
		var url = "http://localhost:5000";
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
		  success: function(){
		  	disp_user();
		  },
		  error: function (request, message, error) {
		  		sessionStorage.clear();
	            window.location.href = '/login';
	         }
		}

		$.ajax(settings);
		
		function disp_user(){
			$( "#nav-username-display" ).html(sessionStorage.getItem('username'));
		}
});