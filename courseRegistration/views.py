from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from datetime import datetime
from .models import *
from taskManager.models import *
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

            #create the Academic task category for the new user
            academicCategory = Category.objects.create(user = currentUser, name = "Academic")
            academicCategory.save()
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
    #initial variables
    currentUser = request.user
    currentUserEx = None
    fullName = ""
    coursesTaken = ""
    new_added_course = None
    existsVal = True
    form = None
    isAdvisor = False

    #if user is actually logged in, not anonymous
    if currentUser.id != None:
        currentUserEx = UserExtended.objects.filter(user = request.user)
        fullName = currentUser.get_full_name()

        if(currentUserEx.exists()):
            currentUserEx = currentUserEx[0]
            isAdvisor = currentUserEx.advisor
            coursesTaken = CourseTaken.objects.filter(user = currentUser)
    
            #add course to list of already taken courses for user
            if request.method == 'POST':
                form = CourseTakenForm(data = request.POST)
                if form.is_valid():
                    #create category object
                    #switch_category = sCategory_form.save(commit=False)
                    addedCourse = form.save(commit=False)
                    addedCourse.user = currentUser
                    addedCourse.save()

                #create the Academic task category for the new user
                academicCategory = Category.objects.create(user = currentUser, name = "Academic")
                academicCategory.save()
            else:
                form = CourseTakenForm()
        else:
            existsVal = False

    return render(
        request, 
        "courseRegistration/profile.html",
        {
            'currentUser': currentUser,
            'currentUserEx': currentUserEx,
            'fullName': fullName,
            'coursesTaken': coursesTaken,
            'existingCourseForm': form,
            'new_added_course': new_added_course,
            'existsVal': existsVal,
            'isAdvisor': isAdvisor,
        }
    )

def courseRegister(request):
    return render(
        request, 
        "courseRegistration/schedulerFinal.html",
        {
            'currentUser':request.user,
        }
    )

def home(request):
    todaysTasks = []
    #if request.user.is_anonymous():
    if request.user.id != None:
        #list of all tasks
        allTasks = Task.objects.filter(user = request.user)
        today = datetime.today()
        todaysTasks = allTasks.filter(endDate__year = today.year, endDate__month = today.month, endDate__day = today.day)
    return render(
        request, 
        "courseRegistration/home.html", 
        {
            'todaysTasks':todaysTasks,
        }
    )