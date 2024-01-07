from django.db import models
from Course.models import Course
from django.contrib.auth.models import User




class Post(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
