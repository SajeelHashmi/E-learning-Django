from django.contrib.auth.models import User
from django.db import models
from Course.models import Course,Assignment

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 40,default = "test")
    phoneNumber = models.CharField(max_length=15)
    registeredCourses = models.ManyToManyField(Course, related_name='RegisteredCourses',null = True,blank=True)
    def __str__(self) -> str:
        return f"{self.name}"
class Submissions(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE,blank = True,null=True)
    submission = models.FileField(upload_to='Submissions',null=True,blank=True)
    checked = models.BooleanField(default=False)
    remarks = models.CharField(max_length=30, null=True,blank=True)
    marksObt = models.IntegerField(null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.student.name}_{self.assignment.id}"
    