import re
class Response:
    def __init__(self, text="Route Not Found", status_code=404)->None:
        self.status_code=status_code
        self.text=text
        self.headers=[]
    def as_wsgi(self, start_response):
       start_response(f"{self.status_code} OK",headers=self.headers)
       return[self.text.encode()]

    def send(self, text, status_code="404"):
        self.status_code=status_code
        self.text=text
        self.headers=[]
        if isinstance (text, str):
            self.text=text
            self.status_code=int(status_code)
        else:
            self.text=str(text)
            self.status_code=int(status_code)
    def render (self, template_name, context={}):
        path=f"{template_name}.html"
        with open(path) as fp:
            template=fp.read()
            for key, value in context.items():
                template = re.sub(r'{{\s*' +re.escape(key)+r'\s*}}', str(value), template)
        self.headers.append(('content-type',"text/html"))
        self.text=template
        self.status_code="200 OK"