from django.shortcuts import render
# Create your views here.
from api.models import UploadImage
import json,base64
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def getdocument(request):
    try:
        return_dict = {}
        if request.is_ajax:
             return_dict['image'] = UploadImage.objects.filter(id=1).first()
             return_dict['image'] = "data:image/jpg;base64,"+return_dict['image'].document
        return HttpResponse(json.dumps(return_dict))
    except:
        import traceback
        traceback.print_exc()
   
def index(request):
    
    return render_to_response('base.html', {}, RequestContext(request))