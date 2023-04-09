/* javascript to accompany jquery.html */
// is this how it knows Im using jQuery?
$(document).ready( 
    // $('form').submit(function(event) {
    /* this defines a function that gets called after the document is in memory */
  function()
  {
    /* !!!HANDER for element addition and deletion */
    $("#element_button").click( 
      function()
      {
		/* ajax post (path, data, callback function) */ //new connection gets made from the browser to the server (post request)
		$.post("/elements_handler.html",
		/* pass a JavaScript dictionary */ //key and value pairs = name: retrieves value (key)
		// keys are always strings in python = but in JS the key is not in quotations
		{
			enum: $("#element_num").val(),	/* retreive value of name field */
			ecode: $("#element_code").val(),
			ename: $("#element_name").val(),
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
    
    /* HANDLER for all sdf document uploads*/
    $("#upload_button").click( 
      function()
      {
    $.post("/sdf_handler.html",
    /* pass a JavaScript dictionary */ //key and value pairs = name: retrieves value (key)
    {
      fp: $("#sdf").val(),
      mname: $("#mol_name").val()
    },
    function( data, status )
    {
      alert( "Data: " + data + "\nStatus: " + status );
      //$("$label").text(data); returns text content of element
    });
      }
	  );

    /* updates element listing*/
    // so its only seeing text/html
    $.ajax({
      url: 'elements.html',
      type: 'GET',
      dataType: 'json',
      success: function(data, status, xhr) {
        if (xhr.getResponseHeader('Content-Type') === 'application/json') {
          // Handle JSON data here
          console.log("hello")
        } else {
          // Handle other data types here
          console.log(xhr.getResponseHeader('Content-Type'))
          console.log(data)
        }
      },
      error: function(xhr, status, error) {
        // Handle error here
        console.log("Goodbye")
      }
    });
  }

)