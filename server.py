from http.server import HTTPServer, BaseHTTPRequestHandler

import io
import sys
import urllib
import json

import MolDisplay
import molsql

public_files = [ '/view.html', '/style.css', '/molecule.js', '/elements.html', 
'/sdf.html', '/molecule.html'];

# ensure you do this only once
db = molsql.Database()
db.create_tables()

class MyHandler( BaseHTTPRequestHandler ):
    # Sends the html file to the server
    def do_GET(self):
        if self.path == '/elements.html':
            if 'application/json' in self.headers.get('Accept'):
                # Get SQLite3 data
                data = db.conn.execute("SELECT * FROM Elements;")
                columns = [column[0] for column in data.description]
                rows = [dict(zip(columns, row)) for row in data.fetchall()]
                json_data = json.dumps(rows)

                # print(json_data)
                
                # Set headers for JSON data
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                # Send JSON data
                self.wfile.write(bytes(json_data, 'utf-8'))
            else:
                fp = open(self.path[1:])
                page = fp.read()
                fp.close()

                # Set headers
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                # Send HTML page
                self.wfile.write(bytes(page, 'utf-8'))

        elif self.path == '/molecule.html':
            if 'application/json' in self.headers.get('Accept'):
                # Get SQLite3 data
                data = db.conn.execute("SELECT * FROM Molecules;")
                columns = [column[0] for column in data.description]
                rows = [dict(zip(columns, row)) for row in data.fetchall()]
                json_data = json.dumps(rows)

                # print(json_data)
                
                # Set headers for JSON data
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                # Send JSON data
                self.wfile.write(bytes(json_data, 'utf-8'))
            else:
                fp = open(self.path[1:])
                page = fp.read()
                fp.close()

                # Set headers
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                # Send HTML page
                self.wfile.write(bytes(page, 'utf-8'))

        elif self.path.endswith(".svg"):
            with open(self.path[1:], "rb") as f:
                svg_data = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header('Content-length', len(svg_data))
            self.end_headers()
            self.wfile.write(svg_data)
            
        elif self.path in public_files: 
            # make sure it's a valid file
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );

            fp = open( self.path[1:] ); 
            # [1:] to remove leading / so that file is found in current dir
            page = fp.read();
            fp.close();

            # create and send headers
            self.send_header( "Content-length", len(page) );
            self.end_headers();

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) );
        else:
            # if the requested URL is not one of the public_files
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "GET 404: not found", "utf-8" ) );

    # implement
    def do_POST(self):
        ### ELEMENT HANDLER FOR DB ###
        # print(self.path)
        if self.path == "/elements_handler.html":

          content_len = int(self.headers.get('content-length', 0))
          post_data = self.rfile.read(content_len)

          # read what was sent 
          print( repr( post_data.decode('utf-8') ) );

          # convert POST content into a dictionary (only function that you need from urllib parse library)
          postvars = urllib.parse.parse_qs( post_data.decode( 'utf-8' ) );

          # parsed what was sent into a dictionary
          print( postvars );
          # NOTE: all the python code is on the server, all JS code on browser (both running at the same time))

          # parsing to remove '#' for radial_gradients svg function
          colour1 = postvars['ecolour1'][0].replace('#', '')
          colour2 = postvars['ecolour2'][0].replace('#', '')
          colour3 = postvars['ecolour3'][0].replace('#', '')

          if int(postvars['eaction'][0]) == 1:
            db['Elements'] = (int(postvars['enum'][0]), postvars['ecode'][0], postvars['ename'][0],
                              colour1, colour2, colour3, int(postvars['eradius'][0]))

            message = f"Element {postvars['ecode'][0]} added to the database"

          elif int(postvars['eaction'][0]) == 0:
            result_set = db.conn.execute( f"""SELECT * FROM Elements WHERE ELEMENT_NO=? AND ELEMENT_CODE=?
            AND ELEMENT_NAME=? AND COLOUR1=? AND COLOUR2=? AND COLOUR3=? AND RADIUS=?""", (int(postvars['enum'][0]),
            postvars['ecode'][0], postvars['ename'][0], colour1, colour2, colour3, postvars['eradius'][0] ) ).fetchall()
            
            if len(result_set) == 0:
                message = f"Element {postvars['ecode'][0]} is not in the database"
            else:
                db.conn.execute( f"""DELETE FROM Elements WHERE ELEMENT_NO=? AND ELEMENT_CODE=?
                AND ELEMENT_NAME=? AND COLOUR1=? AND COLOUR2=? AND COLOUR3=? AND RADIUS=?""", (int(postvars['enum'][0]),
                postvars['ecode'][0], postvars['ename'][0], colour1, colour2, colour3, postvars['eradius'][0] ) )

                # add a way to remove elements
                message = f"Element {postvars['ecode'][0]} removed from the database"
          else:
            message = "No action was provided, therefore no change has been implemented."

          # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )

          self.send_response( 200 ); # OK
          self.send_header( "Content-type", "text/plain" )
          self.send_header( "Content-length", len(message) )
          self.end_headers();

          self.wfile.write( bytes( message, "utf-8" ) )
        else:
            self.send_error(404, 'File Not Found')
        ### HANDLER FOR SDF FILE UPLOADS ###
        if self.path == "/sdf_handler.html":

          content_len = int(self.headers.get('content-length', 0))
          post_data = self.rfile.read(content_len)

          # read what was sent 
          print( repr( post_data.decode('utf-8') ) )
          postvars = urllib.parse.parse_qs( post_data.decode( 'utf-8' ) )
          print( postvars )

          # add the molecule to the database
          fp = open(postvars["fp"][0][12:])
          db.add_molecule( postvars["mname"][0], fp ) 

          message = "molecule added to the database"

          self.send_response( 200 ); # OK
          self.send_header( "Content-type", "text/plain" )
          self.send_header( "Content-length", len(message) )
          self.end_headers();

          self.wfile.write( bytes( message, "utf-8" ) )
        else:
          self.send_error(404, 'File Not Found')        

        if self.path == "/display.html":
            # Parse the uploaded file into a Molecule object
            content_len = int(self.headers.get('content-length', 0))
            post_data = self.rfile.read(content_len)

            # read what was sent 
            print( repr( post_data.decode('utf-8') ) )
            postvars = urllib.parse.parse_qs( post_data.decode( 'utf-8' ) )
            print( postvars )
            
            molecule = postvars["mol"][0]

            # add python libraries and radial gradients
            MolDisplay.radius = db.radius();
            # print(db.radius())
            MolDisplay.element_name = db.element_name();
            MolDisplay.header += db.radial_gradients();

            mol = db.load_mol(molecule)
            mol.sort()
            svg_data = mol.svg()

            # Write the SVG data to a file on the server
            filename = "molecule.svg"
            with open(filename, "w") as f:
                f.write(svg_data)

            # Redirect the client to the URL of the SVG file
            self.send_response(302)
            self.send_header("Location", "/molecule.svg")
            self.end_headers()
    
            self.wfile.write( svg.encode() )
        else:
            self.send_error(404, 'File Not Found')


webform_page = """
<html>
  <head>
    <title> Menu </title>
  </head>
  <body>
    <h1> Molecule Displayer </h1>
      <form action="elements.html" method="post" accept-charset="utf-8">
        <p>
          <input type="submit" value="elementman"/>
      </p>
    </form>
  </body>
</html>"""

webform_page1 = """
<html>
  <head>
    <title> Menu </title>
  </head>
  <body>
    <h1> Molecule Displayer </h1>
    <form action="display" enctype="multipart/form-data" method="post">
      <p>
        <input type="file" id="sdf_file" name="filename"/>
      </p>
      <p>
        <input type="submit" value="Upload"/>
      </p>
    </form>
  </body>
</html>"""

httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
httpd.serve_forever()