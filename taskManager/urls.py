from django.urls import path 
from . import views
from django.contrib import admin

urlpatterns = [
    path('taskpage/', views.taskPage, name='taskPage'),
    path("new_category/", views.addCategory, name="new_category"),
    path("new_task/<slug:category>", views.addTask, name = 'new_task'),
    
]