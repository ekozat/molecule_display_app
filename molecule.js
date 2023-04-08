/* javascript to accompany jquery.html */
// is this how it knows Im using jQuery?
$(document).ready( 
    // $('form').submit(function(event) {
    /* this defines a function that gets called after the document is in memory */
  function()
  {
    /* add a click handler for our button */
    $("#elementbutton").click(
      function()
      {
		/* ajax post (path, data, callback function) */ //new connection gets made from the browser to the server (post request)
		$.post("/elements_handler.html",
		/* pass a JavaScript dictionary */ //key and value pairs = name: retrieves value (key)
		// keys are always strings in python = but in JS the key is not in quotations
		{
			num: $("#elementnum").val(),	/* retreive value of name field */
			code: $("#elementcode").val(),
			name: $("#elementname").val(),
			colour1: $("#colorpicker1").val(),
			colour2: $("#colorpicker2").val(),
			colour3: $("#colorpicker3").val(),
			radius: $("#radius").val(),
			action: $("#action").val()
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