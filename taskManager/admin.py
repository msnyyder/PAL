from django.contrib import admin
from .models import *

# Register your models here.
class CategoryDisplay(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('user', 'name')
admin.site.register(Category, CategoryDisplay)

class TaskDisplay(admin.ModelAdmin):
    list_display = ('user', 'category', 'title', 'content', 'startDate', 'endDate', 'reminderDate', 'notificationsOn')
    search_fields = ('user', 'category', 'title', 'startDate', 'endDate', 'notificationsOn')
admin.site.register(Task, TaskDisplay)
