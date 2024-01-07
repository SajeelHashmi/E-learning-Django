from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.ImageField(upload_to='instructorProfilePics')
    name = models.CharField(max_length=50,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.user.username




class Application(models.Model):
    firstName = models.CharField(max_length= 20,null=True,blank=True)
    lastName = models.CharField(max_length= 20,null=True,blank=True)
    email = models.CharField(max_length= 50,null=True,blank=True)
    description = models.TextField(null=True,blank=True)