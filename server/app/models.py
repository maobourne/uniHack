from django.db import models

# Create your models here.
class Profile(models.Model):
   name = models.CharField(max_length = 50)
   picture = models.ImageField(upload_to = 'static')

class someImage(models.Model):
    image = models.ImageField(upload_to= "photos")
