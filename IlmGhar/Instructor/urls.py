from django.urls import path
from . import views
urlpatterns = [

    path('', views.instructorInfo, name='instructorInfo'),
    path('instructorcourses', views.instructorsCourses, name='instructorsCourses'),
    path('updatebio', views.updateBio, name='updateBio'),
    path('getcoursedata', views.getCourseDate, name='getCourseDate'),
    path('downloadsubmission/<int:lectureId>', views.downloadSubmission, name='downloadSubmission'),
    path('checksubmission/<int:lectureId>', views.checkSubmission, name='checkSubmission'),
    path('new', views.newApplication, name='newApplication'),



  
]