import code
import json

UploadErrorCodes = { 
    "SUCCESS":{'CODE':200,"PREFIX":"Success::","MESSAGE":"Successfuly "},
    "UNKNOWN_ERROR":{"CODE": 501,"PREFIX":"Server error : ","MESSAGE":"Please report to @IT support"}, #Server lacks ability to fulfill
    "VALIDATION_ERROR":{"CODE": 607,"PREFIX":"Validation error : ","MESSAGE":"validation error"},
    "API_ERROR":{"CODE":731,"PREFIX":"Permission error : ","MESSAGE":"API error"},
}

class UploadException(Exception):
    
    def __init__(self, validate_func=None,*args,**kwargs):
        if validate_func:
            if validate_func(args, kwargs):
                self.code = UploadErrorCodes["SUCCESS"]["CODE"]
                if message:
                   self.message =   UploadErrorCodes["SUCCESS"]["prefix"] + message
                else:
                    self.message =   UploadErrorCodes["SUCCESS"]["prefix"] + UploadErrorCodes["SUCCESS"]["message"]
                
    def __str__(self):
        if not self.code:
            raise Exception("Unknown code exception")
        if not self.message:
            raise Exception("Unknown message exception")
        dict_str = {"code":self.code,"message":self.message} 
        if self.code != 200:
            return json.dumps( {"error":dict_str})
        else:
            return json.dumps( {"success":dict_str})


class ValidationException(UploadException):
    def __init__(self,message=None,validate_func=None,*args,**kwargs):
        self.code = UploadErrorCodes["VALIDATION_ERROR"]["CODE"]
        if not message:
            self.message =  UploadErrorCodes["VALIDATION_ERROR"]["PREFIX"]+UploadErrorCodes["VALIDATION_ERROR"]["MESSAGE"]
        else:
            self.message = UploadErrorCodes["VALIDATION_ERROR"]["PREFIX"] + message
        super(ValidationException,self).__init__(validate_func=validate_func,*args,**kwargs)

class APIException(UploadException):
    def __init__(self,message=None,validate_func=None,*args,**kwargs):
        self.code = UploadErrorCodes["API_ERROR"]["CODE"]
        if not message:
            self.message =  UploadErrorCodes["API_ERROR"]["PREFIX"]+UploadErrorCodes["API_ERROR"]["MESSAGE"]
        else:
            self.message = UploadErrorCodes["API_ERROR"]["PREFIX"] + message
        super(APIException,self).__init__(validate_func=validate_func,*args,**kwargs)



class ServerException(UploadException):
    def __init__(self,message=None,validate_func=None,*args,**kwargs):
        self.code = UploadErrorCodes["UNKNOWN_ERROR"]["CODE"]
        if not message:
            self.message =  UploadErrorCodes["UNKNOWN_ERROR"]["PREFIX"]+UploadErrorCodes["UNKNOWN_ERROR"]["MESSAGE"]
        else:
            self.message = UploadErrorCodes["UNKNOWN_ERROR"]["PREFIX"] + message
        super(ServerException,self).__init__(validate_func=validate_func,*args,**kwargs)

