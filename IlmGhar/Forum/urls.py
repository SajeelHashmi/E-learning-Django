from django.urls import path
from . import views
urlpatterns = [

    path('getposts/<int:courseId>', views.getPosts, name='getPosts'),
    path('getreplies/<int:courseId>/<int:postId>', views.getReplies, name='getReplies'),
    path('createpost/<int:courseId>/<int:postId>', views.createPost, name='createPost'),




  
]