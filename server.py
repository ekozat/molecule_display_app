from http.server import HTTPServer, BaseHTTPRequestHandler

import io
import sys
import urllib

import MolDisplay
import molsql

public_files = [ '/view.html', '/style.css', '/molecule.js', '/elements.html', 
'/sdf.html', '/molecule.html'];

class MyHandler( BaseHTTPRequestHandler ):
    # Sends the html file to the server
    def do_GET(self):
        if self.path in public_files: 
            # make sure it's a valid file
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );

            fp = open( self.path[1:] ); 
            # [1:] to remove leading / so that file is found in current dir

            # load the specified file
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

          # ensure you do this only once
          # db = molsql.Database(reset=True)
          # db.create_tables()

          # db['Elements'] = (postvars['num'], postvars['code'], postvars['name'],
          #                   postvars['colour1'], postvars['colour2'], postvars['colour3'],
          #                   postvars['radius'])

          message = "database updated"

          self.send_response( 200 ); # OK
          self.send_header( "Content-type", "text/plain" )
          self.send_header( "Content-length", len(message) )
          self.end_headers();

          self.wfile.write( bytes( message, "utf-8" ) )
        else:
            self.send_error(404, 'File Not Found')

        if self.path == "/display":
            # Parse the uploaded file into a Molecule object
            content_len = int(self.headers.get('content-length', 0))

            for i in range(4):
              next(self.rfile)

            mol = MolDisplay.Molecule()

            # read it in as a textfile
            textFile = io.TextIOWrapper(self.rfile, encoding='utf-8')
            mol.parse(textFile)
            
            # Sort the atoms in the molecule
            mol.sort()
            
            # Generate the SVG for the molecule
            svg = mol.svg()
            
            # Send the SVG to the client
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header('Content-length', len(svg))
            self.end_headers()
            self.wfile.write(svg.encode())
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