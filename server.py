import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):



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