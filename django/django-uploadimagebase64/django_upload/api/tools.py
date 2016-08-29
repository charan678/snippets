from tastypie.api import Api

from api import UploadResource,TestResource

v1_api = Api(api_name='v1')
v1_api.register(UploadResource())
v1_api.register(TestResource())
