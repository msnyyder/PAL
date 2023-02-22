from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
import os

import PALAPP

# Create your views here.
def login(request):
    return render(request, "registration/login.html")


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