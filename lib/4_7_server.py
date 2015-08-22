import web

urls = ('/upload', 'Upload',
        '/response', 'Response')

class Upload:
    def GET(self):
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="" name="uploadFile">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(myfile={})
        web.debug(x['myfile'].filename) # This is the filename
        web.debug(x['myfile'].value) # This is the file contents
        web.debug(x['myfile'].file.read()) # Or use a file(-like) object
        # raise web.internalerror()
        raise web.seeother('/response')

class Response:
    def GET(self):
        return """<html><head></head><body>
<h1>hola</h1>
</body></html>"""

def main():
   app = web.application(urls, globals())
   app.run()


if __name__ == "__main__":

    main()
