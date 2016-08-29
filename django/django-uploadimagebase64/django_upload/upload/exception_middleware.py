import json
from django.core import exceptions
from upload.exceptions import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from exceptions import *
import traceback
from colorama import Fore, init
from django.template import RequestContext

        
class ExceptionMiddleware(object):
    
    
    def __init__(self):
        self.ALERT_TUPLE = (GeneratorExit,KeyboardInterrupt,SystemExit,StopIteration,StandardError,ArithmeticError,FloatingPointError,OverflowError,ZeroDivisionError
                       ,AssertionError,AttributeError,EnvironmentError,IOError,OSError,EOFError,ImportError
                       ,LookupError,IndexError,KeyError,MemoryError,NameError
                       ,UnboundLocalError,ReferenceError,RuntimeError,NotImplementedError,SyntaxError,IndentationError
                       ,TabError,SystemError,TypeError,ValueError)
        
        super(ExceptionMiddleware,self).__init__()
    
    
    def process_exception(self,request, exception):
        init()
        print "$$$"*100
    
        if type(exception) == exceptions.ValidationError:
            exception = ValidationException(message=exception.message)
        
        elif type(exception) == BaseException:
            exception = ServerException(message="Unknown Exception please contact Itsupport")
        
        elif type(exception) ==  UploadException or issubclass(type(exception), UploadException):
            pass   
        else:
            if type(exception) in self.ALERT_TUPLE:
                print Fore.RED
            exception = ServerException(message="Unknown Exception please contact Itsupport")
    
        traceback.print_exc()
        print Fore.RESET
       
        print "*"*30
        print request.META
        print "#"*30
        
        if request.META.get("HTTP_REQUEST_SOURCE",False):           
            return HttpResponse(exception)
        
        if request.is_ajax():
            return HttpResponse(exception)
        
       
        
        else:
            return self.jadeRenderError(request,exception.code,exception.message)
    
    def jadeRenderError(self,request,code,message):
        return render_to_response("error.html",{"code":code,"message":message},RequestContext(request))
    
    
    
    
    
