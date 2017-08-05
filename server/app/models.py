from django.db import models

# Create your models here.
class Profile(models.Model):
   name = models.CharField(max_length = 50)
   picture = models.ImageField("img", upload_to = 'static')

class someImage(models.Model):
    pic = models.ImageField(upload_to= "app/img")
