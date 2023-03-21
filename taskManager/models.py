from django.db import models
from django.contrib.auth.models import User
from datetime import date

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
    startDate = models.DateTimeField(default= date.today)
    endDate = models.DateTimeField(default= date.today)
    reminderDate = models.DateTimeField(default = date.today)
    notificationsOn = models.BooleanField(default=True)

    def __str__(self):
        return self.title