import json, datetime, urllib2, jsonschema, base64, pycountry, re, copy, phonenumbers, difflib, \
urllib, hashlib, random, os, pytz, calendar, ast, math, ipaddress

# Tastypie import
from tastypie.authentication import Authentication, SessionAuthentication
from tastypie import fields
from tastypie.constants import ALL
from tastypie.authorization import Authorization
from tastypie.resources import ObjectDoesNotExist
from tastypie.bundle import Bundle
from tastypie.throttle import BaseThrottle
from tastypie.resources import Resource, ModelResource
from tastypie.exceptions import ImmediateHttpResponse, BadRequest, ApiFieldError
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils.cache import patch_cache_control
from models import UploadImage,TestModel

   
class APPModelResource(ModelResource):
    def wrap_view(self, view):
        
        super(APPModelResource,self).wrap_view( view)
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            callback = getattr(self, view)
            response = callback(request, *args, **kwargs)
            if request.is_ajax():
                patch_cache_control(response, no_cache=True)
            return response
         
        return wrapper
    

#############################################PROCESSOR APIS######################################################################
class UploadResource(APPModelResource):
    class Meta:
        object_class = UploadImage
        authorization = Authorization()
        resource_name = 'upload'
        queryset = UploadImage.objects.all()
        always_return_data = True
        allowed_methods = ['post']
        
    def obj_create(self, bundle, **kwargs):
        input_data = bundle.data
        input_data["comments"] = 'Document Upload'
        image = input_data['id_image'][0].read()
        input_data["document"]=  base64.b64encode(image)
        bundle.data = input_data
        return super(UploadResource,self).obj_create(bundle, **kwargs)
            
    
    def deserialize(self, request, data, format = None, perm_checked=False):
        if format.startswith('multipart'):
            input_data = request.POST.dict()
            if request.FILES:     
                input_data['id_image'] = [request.FILES.get('id_image')]
                return input_data
        return super(UploadResource, self).deserialize(request, data, format)

class TestResource(ModelResource):
     
    class Meta:
        object_class = TestModel
        authorization = Authorization()
        resource_name = 'test'
        queryset = TestModel.objects.all()
        always_return_data = True
        allowed_methods = ['post']
        
    def obj_create(self, bundle, **kwargs):    
        #res = UploadResource()
        #request_bundle = res.deserialize(bundle.request, bundle.data, format = "application/json", 
        #                                     perm_checked = True)
        return super(TestResource,self).obj_create(bundle, **kwargs)
        
     
     
     
     
        
        