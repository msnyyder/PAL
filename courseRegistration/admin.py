from django.contrib import admin
from .models import *

#display all extended users
class ExtendedUserDisplay(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'netId', 'netPassword', 'takenCourses', 'major')
    search_fields = ('user', 'major')
admin.site.register(UserExtended, ExtendedUserDisplay)

#display all schedules
class ScheduleDisplay(admin.ModelAdmin):
    list_display = ('name', 'semester', 'year', 'courses')
    search_fields = ('name', 'semster', 'year')
admin.site.register(Schedule, ScheduleDisplay)

class RealScheduleDisplay(admin.ModelAdmin):
    list_display = ('grades',)
admin.site.register(RealSchedule, RealScheduleDisplay)

class DraftScheduleDisplay(admin.ModelAdmin):
    list_display = ('advisorNotes', 'draftRanking')
    search_fields = ('draftRanking',)
admin.site.register(DraftSchedule, DraftScheduleDisplay)

#display all courses
class CourseDisplay(admin.ModelAdmin):
    list_display = ('title', 'crn', 'creditHours', 'description')
    search_fields = ('crn', 'title', 'creditHours')
admin.site.register(Course, CourseDisplay)
