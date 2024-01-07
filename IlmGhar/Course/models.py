from django.db import models
from Instructor.models  import  Instructor

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Language(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Course(models.Model):
    # maybe add an introductory video to each course
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE,null=True,blank=True)
    language = models.ForeignKey(Language,on_delete = models.DO_NOTHING,null= True,blank=True)
    coverPic = models.ImageField(upload_to='CourseCoverPics',null = True, blank = True, default = None)
    title = models.CharField(max_length=100)
    description = models.TextField()
    subject = models.ForeignKey(Subject,on_delete = models.DO_NOTHING,null= True,blank=True)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.title
    
class Lecture(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField(default = "default")
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    videoFile = models.FileField(upload_to="LectureVideos",null=True,blank=True)
    # this seems to be malfunctioning we are simply going to store the hls files
    # inside a directory of the lectureVideos directory with the naming scheme f"{lecture.title}_{lecture.id}__hls"
    # then we can simply access the files in our view by getting the location from the videoFile field
    # and appending the naming scheme to get the hls dir 
    # hlsDir = models.FilePathField(null=True,blank=True)
    notes = models.FileField(upload_to='LectureNotes',null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.title}_{self.course.title}"

class Assignment(models.Model):
    lecture = models.OneToOneField(Lecture,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='AssignmentFiles')
    marks = models.IntegerField(default=0)
    def __str__(self) -> str:
        return f"{self.title}_{self.lecture.course.title}"