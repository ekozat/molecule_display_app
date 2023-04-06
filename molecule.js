/* javascript to accompany jquery.html */
// is this how it knows Im using jQuery?
$(document).ready( 
    // $('form').submit(function(event) {
    /* this defines a function that gets called after the document is in memory */
  function()
  {

    /* add a click handler for our button */
    $("#elementAdd").submit(
      function()
      {
	/* ajax post (path, data, callback function) */ //new connection gets made from the browser to the server (post request)
	$.post("/elements_handler.html",
	  /* pass a JavaScript dictionary */ //key and value pairs = name: retrieves value (key)
	  // keys are always strings in python = but in JS the key is not in quotations
	  {
	    num: $("#elementnum").val(),	/* retreive value of name field */
	    extra_info: "some stuff here"
	  },
	  function( data, status )
	  {
	    alert( "Data: " + data + "\nStatus: " + status );
		//$("$label").text(data); returns text content of element
	  }
	);
      }
    );
  }

)