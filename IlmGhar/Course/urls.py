from django.urls import path
from . import views
urlpatterns = [

    path('allcourses', views.allCourses, name='AllCourses'),
    path('languages', views.getLanguages, name='getLanguages'),
    path('subjects', views.getSubjects, name='getSubjects'),
    path('tags', views.getTags, name='getTags'),

    path('threebylang/<str:language>', views.getFirstThreeByLanguage, name='threeByLang'),
    path('<int:id>',views.getCourse,name="getCourse"),
    path('registered/<int:id>',views.getRegistered,name="getRegistered")

]