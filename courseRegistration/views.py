from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from .models import *
from .forms import *
import os

import PALAPP

# Create your views here.
def login(request):
    return render(request, "registration/login.html")

def profile(request):
    currentUser = request.user
    currentUserEx = UserExtended.objects.filter(user = request.user)[0]

    coursesTaken = currentUserEx.takenCourses.split(",")
    
    #add course to list of already taken courses for user
    new_added_course = None
    if request.method == 'POST':
        form = ExistingCourseForm(data = request.POST)
        if form.is_valid():
            #create category object
            #switch_category = sCategory_form.save(commit=False)
            addedCourse = form.cleaned_data['allCourses']

            #switch_category.save()
            new_added_course = Course.objects.filter(title = addedCourse)[0]
            currentUserEx.takenCourses = currentUserEx.takenCourses + new_added_course.title + ", "
            currentUserEx.save()

    else:
        form = ExistingCourseForm()

    return render(
        request, 
        "courseRegistration/profile.html",
        {
            'currentUser': currentUser,
            'currentUserEx': currentUserEx,
            'fullName': currentUser.get_full_name(),
            'coursesTaken': coursesTaken,
            'existingCourseForm': form,
            'new_added_course': new_added_course,
        }
    )


def courseRegister(request):
    return render(
        request, 
        "courseRegistration/scheduler.html", 
        {
            'currentUser':request.user,
        }
    )

def home(request):
    return render(
        request, 
        "courseRegistration/home.html", 
    )