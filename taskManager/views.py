from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404


# Create your views here.
def taskPage(request):
    #get all of the current user's categories 
    categories = Category.objects.filter(user = request.user)
    #get all tasks for default category group
    defaultCategory = Category.objects.filter(name = "Academic")

    #automatically create Academic category if it does not exist
    defaultCategory = defaultCategory[0]

    taskstemp = Task.objects.filter(category = defaultCategory)
    tasks = taskstemp.filter(user = request.user)

    return render(
        request,
        "taskManager.html",
        {
            'currentUser': request.user,
            'categories': categories,
            'tasks': tasks,
            'chosenCategory': defaultCategory,
        }
    )

#switch the category and show all tasks within selected category
def switchCategory(request, category):
    #get all of the current user's categories for selected category
    categories = Category.objects.filter(user = request.user)
    category = categories.filter(name = category)

    taskstemp = Task.objects.filter(category = category)
    tasks = taskstemp.filter(user = request.user)

    return render(
        request,
        "taskManager.html",
        {
            'currentUser': request.user,
            'categories': categories,
            'tasks': tasks,
            'chosenCategory': category,
        }
    )
