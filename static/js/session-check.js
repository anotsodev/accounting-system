$( document ).ready(function() {
		var url = "http://10.5.92.201:5000";
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
		  		alert('You are not logged in or session has expired. Please login again.');
		  		sessionStorage.clear();
	            window.location.href = '/login';
	         }
		}

		$.ajax(settings).done(function (response) {
		  console.log(response);
		});
});