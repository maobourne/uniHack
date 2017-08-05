from django.db import models

# Create your models here.
class Profile(models.Model):
   name = models.CharField(max_length = 50)
<<<<<<< HEAD
   picture = models.ImageField(upload_to = 'temp_photo')
=======
   picture = models.ImageField(upload_to = 'static')
>>>>>>> 58c7cd32306289809a273a453626fbf39f5acb7d





class someImage(models.Model):
    image = models.ImageField(upload_to= "photos")
