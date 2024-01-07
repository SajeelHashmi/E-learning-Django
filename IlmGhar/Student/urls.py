from django.urls import path
from . import views
urlpatterns = [

    path('registeredcourses', views.registeredCourses, name='registeredCourses'),
    path('registernewcourse/<int:id>', views.registernNewCourse, name='registernNewCourse'),
    path('suggested', views.suggestedCourse, name='suggestedCourse'),

    path('', views.studentInfo, name='studentInfo'),
    path('downloadassignment/<int:courseId>', views.downloadAssignment, name='downloadAssingment'),
    path('downloadnotes/<int:courseId>', views.downloadNotes, name='downloadAssingment'),
    path('downloadsubmission/<int:courseId>', views.downloadSubmission, name='downloadAssingment'),

    # submit assingment view
    path('submit/<int:assingmentId>', views.submitAssingment, name='submitAssingment'),
    path('lecture/<int:courseId>/<int:lectureId>', views.getLectureInfo, name='returnM3U8'),

    path('getregisteredcourse', views.getRegisteredCourse, name='getRegisteredCourse'),
    path('lecture/<int:courseId>/<int:lectureId>/output.m3u8/', views.returnM3U8, name='returnM3U8'),
    path('lecture/<int:courseId>/<int:lectureId>/output.m3u8/<str:segmentName>', views.playLecture, name='playLecture'),

    # path("",views.home,name="home"),
]