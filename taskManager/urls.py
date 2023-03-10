from django.urls import path 
from . import views
from django.contrib import admin

urlpatterns = [
    path('taskpage/', views.taskPage, name='taskPage'),
    
]