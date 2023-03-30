from urllib import request
from .models import *
from django import forms
from django.forms import Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ExistingCourseForm(Form):
    allCourses = forms.ModelChoiceField(queryset = Course.objects.all())