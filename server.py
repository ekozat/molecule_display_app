import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        if self.path == "/"
            self.send_response(200) # OK response
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len(webform_page) )
            self.end_headers()

            self.wfile.write( bytes( webform_page, "utf-8" ))

        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )

    #def DO_POST(self):



webform_page = """
<html>
    <head>
        <title> File Upload </title>
    </head>
    <body>
        <h1> File Upload </h1>
        <form action="molecule" enctype="multipart/form-data" method="post">
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