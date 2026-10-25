from typing import Any
import types
import inspect
from responsef import Response
from parse import parse
from request import Request
SUPPORTED_REQ_METHOD={'GET','POST','DELETE'}

class slowapi:
    def __init__(self, middlewear)->None:
        self.routes = dict()
        self.middlewear=middlewear
        self.middlewear_for_routes= dict()
    def __call__(self, environ, start_response)-> Any:
        response = Response()
        request=Request(environ)
        for middlewear in self.middlewear:
            if isinstance (middlewear, types.FunctionType):
                 middlewear(request)
            else:
                 raise ValueError("only fucntions can be passed in thsi twin")
        for path,handler_method in self.routes.items():
            res=parse(path, request.path_info)
            for request_method,handler in handler_method.items():
                if request.request_method==request_method and res:
                    route_mw_list = self.middlewear_for_routes[path][request_method]
                    for mw in route_mw_list:
                         if isinstance (mw, types.FunctionType):
                              mw(request)
                         else:
                            raise ValueError ("only functions lil bro")
                    handler(request, response, **res.named)
                    return response.as_wsgi(start_response)
        return response.as_wsgi(start_response)

    def route_common(self, path,handler,method_name, middlewear):
                    path_name=path or f"/{handler.__name__}"
                    if path_name not in self.routes:
                        self.routes[path_name]={}
                    self.routes[path_name][method_name]= handler
                    if path_name not in self.middlewear_for_routes:
                         self.middlewear_for_routes[path_name]={}
                    self.middlewear_for_routes[path_name][method_name]=middlewear
                    return handler

    def get(self, path=None,middlewear=[]):
        def wrapper(handler):
            return self.route_common(path,handler,'GET',middlewear)
        return wrapper
    
    def post(self, path=None,middlewear=[]):
        def wrapper(handler):
            return self.route_common(path,handler,'POST',middlewear)
        return wrapper
    
    def delete(self, path=None,middlewear=[]):
        def wrapper(handler):
            return self.route_common(path,handler,'DELETE',middlewear)
        return wrapper
    
    def route(self, path=None, middlewear=[]):
        def wrapper(handler):
            if isinstance (handler, type):
                 class_members = inspect.getmembers(handler, lambda x: inspect.isfunction(x)and not(
                      x.__name__.startswith("__")and x.__name__.endswith("__")) and
                        x.__name__.upper() in SUPPORTED_REQ_METHOD)
                 print(class_members)
                 for fn_name, fn_handler in class_members:
                      self.route_common (path or f"/{handler.__name__}",fn_handler,fn_name.upper(),middlewear)
            else:
                 raise ValueError("ts aint class twin")
        return wrapper