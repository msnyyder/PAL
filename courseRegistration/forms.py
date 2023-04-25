from urllib import request
from .models import *
from django import forms
from django.forms import Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#class ExistingCourseForm(Form):
#    allCourses = forms.ModelChoiceField(queryset = Course.objects.all())

class ModifyCourse(Form):
    Choices = (
        ('add', 'Add'),
        ('remove', 'Remove')
    )
    course = forms.CharField(label="Course", max_length=10)
    addStatus = forms.ChoiceField(label = "Add or Remove", widget=forms.Select, choices = Choices)

class RegisterForm(Form):
    ACT = forms.BooleanField(label='ACT', required=False)
    MPE = forms.BooleanField(label='MPE', required=False)

class CourseTakenForm(forms.ModelForm):
    class Meta:
        model = CourseTaken
        fields = ('course',)

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class NewExtendedUserForm(forms.ModelForm):
    class Meta:
        model = UserExtended
        fields = ('advisor', 'netId', 'major')
        