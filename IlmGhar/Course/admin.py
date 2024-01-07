from django.contrib import admin
from .models import *

class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class LectureAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Lecture,LectureAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Subject)
admin.site.register(Assignment)




