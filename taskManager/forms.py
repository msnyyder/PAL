from .models import *
from django import forms
from django.forms import Form

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





