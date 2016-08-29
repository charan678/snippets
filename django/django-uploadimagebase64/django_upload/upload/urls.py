from django.conf.urls import include, url
from views import getdocument,index


urlpatterns = [
    url(r'^getdocument/', getdocument),
    url(r'^index/', index),
]
