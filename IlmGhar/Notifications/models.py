from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content  = models.TextField(null= True,blank = True)
    associatedLink  = models.TextField(null= True,blank = True)
    read = models.BooleanField(default = False)
    def __str__(self):
        return f"{self.user.username}  {self.content}"
