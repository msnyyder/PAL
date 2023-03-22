from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'content', 'startDate', 'endDate', 'notificationsOn', 'reminderDate')