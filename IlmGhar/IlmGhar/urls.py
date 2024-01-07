from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/login/", include('Login.urls')),
    path('api/courses/',include('Course.urls')),
    path('api/student/',include('Student.urls')),
    path('api/instructor/',include('Instructor.urls')),
    path('api/forum/',include('Forum.urls')),
    path('api/notification/',include('Notifications.urls')),
    # path("api/",views.home,name="home"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
