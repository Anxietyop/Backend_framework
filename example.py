from main import slowapi
from request import Request
def global_middlewear(request):
   print("this was executed before any route")
slow = slowapi(middlewear=[global_middlewear])

def local_middlewear(reqest):
   print("hey this was here")

@slow.get('/users/{id}', middlewear =[local_middlewear])
def get_users(req, res, id):
   res.send("Rivaan", 200)

#@slow.post('/users')
#def get_users(req,res):
 #  res.send("Hey There",200)

@slow.route("/users", middlewear=[local_middlewear])
class User:
   def __init__(self):
      pass
   def get(req, res):
      print(req.queries)
      res.send("Test 12",200)

   def post(req, res):
      res.render("example", {"name":"name", "message":"ITS DONNEEEE"})