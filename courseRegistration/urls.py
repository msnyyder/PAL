from django.urls import path 
from . import views
from django.contrib import admin


urlpatterns = [
    path('courseregister/', views.courseRegister, name='scheduler'),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("", views.home, name = "home"),
]