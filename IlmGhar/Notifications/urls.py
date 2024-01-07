from django.urls import path
from . import views
urlpatterns = [

    path('get', views.getNotifications, name='getNotifications'),
    path('markasread/<int:id>', views.markAsRead, name='markAsRead'),
    path('deletenotification/<int:id>', views.deleteNotification, name='deleteNotification'),
    path('count', views.count, name='count'),

]