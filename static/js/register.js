$(document).ready(function () {

	function register(){
	
		var first = document.forms["registerForm"]["firstName"].value;
		var last = document.forms["registerForm"]["lastName"].value;
		var user = document.forms["registerForm"]["user"].value;
		var pass = document.forms["registerForm"]["pass"].value;
		var cpass = document.forms["registerForm"]["cpass"].value;
		var email = document.forms["registerForm"]["email"].value;
		var phone = document.forms["registerForm"]["pnumber"].value;
		var balance = document.forms["registerForm"]["balance"].value;

	    if (first == "" || last == "" || user == "" || pass == "" || cpass == "" || email == "" || phone == "" || balance == "") {
	        alert("Fields must be filled out");
	        //return false;
	    }
	    else{
	    	console.log(first, last);
			window.location.replace("http://stackoverflow.com");

	    }
		//if(){
	     //window.location.href = "http://example.com";
		//}
	}

})
