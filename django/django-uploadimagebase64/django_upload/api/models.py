from django.db import models
from django.db.models.fields import TextField
from django.contrib.auth.models import User



class UploadImage(models.Model): # models.IntegerField() models.DateTimeField()
    class Meta:
        db_table = 'uploadimage'
        app_label = 'api'   
    document = TextField()
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False) # DateTime when document was uploaded
    comments = models.TextField(null=True)

class TestModel(models.Model): # models.IntegerField() models.DateTimeField()
    class Meta:
        db_table = 'test'
        app_label = 'api'   
    test = models.TextField(null=True)
    
    