from urllib import request
from .models import *
from django import forms
from django.forms import Form
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
        widgets = {'startDate':forms.SelectDateWidget, 'endDate':forms.SelectDateWidget, 'reminderDate':forms.SelectDateWidget}

class SwitchCategoryForm(Form):
    def __init__(self, user, *args, **kwargs):
        super(SwitchCategoryForm, self).__init__(*args, **kwargs)
        self.user = user
        CHOICES = Category.objects.filter(user=self.user).distinct().values('name')
        CHOICES = [(choice['name'], choice['name']) for choice in CHOICES]
        self.fields['allCategories'] = forms.ChoiceField(choices=CHOICES, required=True)
    #allCategories = forms.ModelChoiceField(queryset = Category.objects.all())
    #allCategories = forms.ModelChoiceField(queryset = Category.objects.filter(user__id = 1))
    




