from django.contrib import admin
from .models import *

class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Student,StudentAdmin)
admin.site.register(Submissions)