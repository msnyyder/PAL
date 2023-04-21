from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from datetime import datetime


# Create your views here.
def taskPage(request):
    #get all of the current user's categories 
    categories = Category.objects.filter(user = request.user)
    #get all tasks for default category group
    defaultCategory = Category.objects.filter(name = "Academic", user = request.user)

    #automatically create Academic category if it does not exist
    switch_category = defaultCategory[0]
    
    #get selected option from dropdown menu
    #if request.GET.get('dropdown') != None:
    #    switch_category = request.GET.get('dropdown')
    
    if request.method == 'POST':
        sCategory_form = SwitchCategoryForm(data = request.POST)
        if sCategory_form.is_valid():
            #create category object
            #switch_category = sCategory_form.save(commit=False)
            oneName = sCategory_form.cleaned_data['allCategories']
            #switch_category.save()
            switch_category = Category.objects.filter(name = oneName, user = request.user)[0]

    else:
        sCategory_form = SwitchCategoryForm()

    #list of all tasks
    taskstemp = Task.objects.filter(category = switch_category)
    tasks = taskstemp.filter(user = request.user)

    #list of all the enddates for every task
    listOfDays = tasks.values('endDate')

    #values for the current date
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    amountOfDays = getDays(currentMonth, currentYear)

    task_days = tasks.filter(endDate__month__gte = currentMonth)

    #get first day of the week (weekday) for calendar
    firstDate = datetime(currentYear, currentMonth, 1)
    startWeekDay = firstDate.weekday()

    return render(
        request,
        "taskManager.html",
        {
            'currentUser': request.user,
            'categories': categories,
            'tasks': tasks,
            'chosenCategory': switch_category,
            'form': sCategory_form,
            'days': amountOfDays,
            'month': currentMonth,
            'currentDay': currentDay,
            'currentYear': currentYear,
            'listOfDays': listOfDays,
            'startWeekDay':startWeekDay,
            'taskDays' : task_days,
        }
    )

#Create a new category
def addCategory(request):
    new_category = None
    #A new category is created
    if request.method == 'POST':
        category_form = CategoryForm(data = request.POST)
        if category_form.is_valid():
            #create category object
            new_category = category_form.save(commit=False)
            #assign current user to category
            new_category.user = request.user
            #Save category to database
            new_category.save()
    else:
        category_form = CategoryForm()

    return render(
        request,
        "newCategory.html",
        {
            'currentUser': request.user,
            'new_category': new_category,
            'category_form': category_form,
        }
    )

#Create a new task
def addTask(request, category):
    #get all of the current user's categories for selected category
    categories = Category.objects.filter(user = request.user)
    cat = categories.filter(name = category)
    cat = cat[0]
    
    new_task = None
    #A new category is created
    if request.method == 'POST':
        task_form = TaskForm(data = request.POST)
        if task_form.is_valid():
            #create category object
            new_task = task_form.save(commit=False)
            #assign current user to category
            new_task.user = request.user
            new_task.category = cat
            #Save category to database
            new_task.save()
    else:
        task_form = TaskForm()

    return render(
        request,
        "newTask.html",
        {
            'currentUser': request.user,
            'new_task': new_task,
            'task_form': task_form,
        }
    )

#get the amount of days in the current month
def getDays(month, year):
    if(month == 2):
        if(year % 400 == 0 or (year % 100 != 0 and year % 4 == 0)):
            #is a leap year
            days = 29
        else:
            #is not a leap year
            days = 28
    elif(month == 4 or month == 6 or month == 9 or month == 11):
        days = 30
    else:
        days = 31   
    return days