from django.db import models
from django.contrib.auth.models import User
from datetime import date

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Create your models here.
#Table for Categories
class Category(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='user_category')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
#Table for tasks
class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='user_task')
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING,related_name='task_category')
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    startDate = models.DateTimeField(auto_now_add=False)
    endDate = models.DateTimeField(auto_now_add=False)
    reminderDate = models.DateTimeField(auto_now_add=False)
    notificationsOn = models.BooleanField(default=True)

    def __str__(self):
        return self.title