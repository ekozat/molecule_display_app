/* javascript to accompany jquery.html */
// is this how it knows Im using jQuery?
$(document).ready( 
    // $('form').submit(function(event) {
    /* this defines a function that gets called after the document is in memory */
  function()
  {
    /* !!!HANDER for element addition and deletion */
    $("#elementbutton").click( 
      function()
      {
		/* ajax post (path, data, callback function) */ //new connection gets made from the browser to the server (post request)
		$.post("/elements_handler.html",
		/* pass a JavaScript dictionary */ //key and value pairs = name: retrieves value (key)
		// keys are always strings in python = but in JS the key is not in quotations
		{
			enum: $("#elementnum").val(),	/* retreive value of name field */
			ecode: $("#elementcode").val(),
			ename: $("#elementname").val(),
			ecolour1: $("#colorpicker1").val(),
			ecolour2: $("#colorpicker2").val(),
			ecolour3: $("#colorpicker3").val(),
			eradius: $("#radius").val(),
			eaction: $("#action").val()
		},
		function( data, status )
		{
			alert( "Data: " + data + "\nStatus: " + status );
			//$("$label").text(data); returns text content of element
		}
		).fail(function(err, status) {
			alert("Something went wrong");
			// something went wrong, check err and status
	 	});
      }
    );
  }

)