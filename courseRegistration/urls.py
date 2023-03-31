from django.urls import path 
from . import views
from django.contrib import admin


urlpatterns = [
    path('courseregister/', views.courseRegister, name='scheduler'),
    path("login/", views.login, name="login"),
    path("register/", views.new_user, name="new_user"),
    path("register2/", views.new_user2, name="new_user2"),
    path("profile/", views.profile, name="profile"),
    path("", views.home, name = "home"),
]