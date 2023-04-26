from django.contrib import admin
from .models import *

#display all extended users
class ExtendedUserDisplay(admin.ModelAdmin):
    list_display = ('user', 'advisor', 'phone_number', 'netId', 'netPassword', 'major')
    search_fields = ('user', 'major', 'advisor')
admin.site.register(UserExtended, ExtendedUserDisplay)

#display all courses taken
class CoursesTakenDisplay(admin.ModelAdmin):
    list_display = ('user', 'course')
    search_fields = ('user', 'course')
admin.site.register(CourseTaken, CoursesTakenDisplay)

