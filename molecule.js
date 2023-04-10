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
        console.log("hello");
              //$("$label").text(data); returns text content of element
          }
          ).fail(function(err, status) {
              alert("Something went wrong");
        console.log("goodbye");
              // something went wrong, check err and status
           });
        }
      );
  
      /* updates element listing*/
      $.ajax({
        url: 'elements.html',
        type: 'GET',
        dataType: 'json',
        success: function(data, status, xhr) {
        if (xhr.getResponseHeader('Content-Type') === 'application/json') {
            // Handle JSON data here
            var table = $('#table_elements');
            for (var i = 0; i < data.length; i++) {
            var element = data[i]
  
            var string = '<tr><td>' + element["ELEMENT_NO"] + '</td><td>' + 
            element["ELEMENT_CODE"] + '</td><td>' + element["ELEMENT_NAME"] + 
            '</td><td>' + element["COLOUR1"] + '</td><td>' + element["COLOUR2"] +
            '</td><td>' + element["COLOUR3"] + '</td><td>' + element["RADIUS"];
  
            table.append(string);
            }
  
        } else {
            // Handle other data types here
            console.log(xhr.getResponseHeader('Content-Type'))
            console.log(data)
        }
        },
        error: function(xhr, status, error) {
        // Handle error here
        console.log('Error: ' + status + ' - ' + error);
        }
      });

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


    /* HANDLER for molecule display*/
    $("#display_button").click( 
        function()
        {
            $.post("/display.html",
            /* pass a JavaScript dictionary */ //key and value pairs = name: retrieves value (key)
            {
                mol: $("#mol_choice").val()
            },
            function( data, status )
            {
                alert( "Data: " + data + "\nStatus: " + status );
                console.log(data);
                //$("$label").text(data); returns text content of element
            }).fail(function(data, err, status){
                console.log("Err: " + err.responseText + "\nStatus: " + status);
            });
        }
    );

    /* updates molecule listing*/
    $.ajax({
        url: 'molecule.html',
        type: 'GET',
        dataType: 'json',
        success: function(data, status, xhr) {
        if (xhr.getResponseHeader('Content-Type') === 'application/json') {
            // Handle JSON data here
            console.log("hello")
            var options = $('#mol_choice');
            for (var i = 0; i < data.length; i++) {
            var molecule = data[i]

            var string = '<option value=' + molecule["NAME"] + '>' +
            molecule["NAME"] + '</options>';

            options.append(string);
            }

        } else {
            // Handle other data types here
            console.log(xhr.getResponseHeader('Content-Type'))
            console.log(data)
        }
        },
        error: function(xhr, status, error) {
        // Handle error here
        console.log('Error: ' + status + ' - ' + error);
        }
    });
    
})