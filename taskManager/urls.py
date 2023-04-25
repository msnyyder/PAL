from django.urls import path 
from . import views

urlpatterns = [
    path('taskpage/', views.taskPage, name='taskPage'),
    path("new_category/", views.addCategory, name="new_category"),
    path("new_task/<slug:category>", views.addTask, name = 'new_task'),
    path('taskpage/chat/', views.lobby),
    path('taskpage/chat/room/', views.room),
    path('taskpage/chat/get_token/', views.getToken),

    path('taskpage/chat/create_member/', views.createMember),
    path('taskpage/chat/get_member/', views.getMember),
    path('taskpage/chat/delete_member/', views.deleteMember),
]