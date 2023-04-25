from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('courseregister/', views.courseRegister, name='scheduler'),
    path('courseregister/addCourse/', views.addCourse, name='addCourse'),
    path('courseregister/schedule/', views.schedule, name='schedule'),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.new_user, name="new_user"),
    path("register2/", views.new_user2, name="new_user2"),
    path("profile/", views.profile, name="profile"),
    path("", views.home, name = "home"),
]