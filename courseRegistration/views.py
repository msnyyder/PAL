from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
import logging
from .models import *
from .forms import *
import os

import PALAPP

# Create your views here.
def login(request):
    return render(request, "registration/login.html")

#add a new user to user and extended user class
def new_user(request):
    template_name = "courseRegistration/new_user.html"
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request)
            messages.success(request, "Registration Successful")
            #return new_user2(request)
        else:
            messages.error(request, "Unsuccessful Registration: Invalid Information")
    form = NewUserForm()
    return render(request, template_name, context={"register_form":form})

def new_user2(request):
    currentUser = request.user

    new_user = None
    #A new category is created
    if request.method == 'POST':
        user_form = NewExtendedUserForm(data = request.POST)
        if user_form.is_valid():
            #create category object
            new_user = user_form.save(commit=False)
            #assign current user to category
            new_user.user = request.user
            new_user.save()
    else:
        user_form = NewExtendedUserForm()

    return render(
        request,
        "courseRegistration/new_user2.html",
        {
            'currentUser': currentUser,
            'new_user': new_user,
            'user_form': user_form,
        }
    )

def profile(request):
    currentUser = request.user
    currentUserEx = UserExtended.objects.filter(user = request.user)

    coursesTaken = ""
    new_added_course = None
    existsVal = True
    form = None

    if(currentUserEx.exists()):
        currentUserEx = currentUserEx[0]
        coursesTaken = currentUserEx.takenCourses.split(",")
    
        #add course to list of already taken courses for user
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
    else:
        existsVal = False

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
            'existsVal': existsVal,
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