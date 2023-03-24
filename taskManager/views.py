from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404


# Create your views here.
def taskPage(request):
    #get all of the current user's categories 
    categories = Category.objects.filter(user = request.user)
    #get all tasks for default category group
    defaultCategory = Category.objects.filter(name = "Academic")

    #automatically create Academic category if it does not exist
    switch_category = defaultCategory[0]
    
    #get selected option from dropdown menu
    if request.GET.get('dropdown') != None:
        switch_category = request.GET.get('dropdown')

    if request.method == 'POST':
        sCategory_form = SwitchCategoryForm(data = request.POST)
        if sCategory_form.is_valid():
            #create category object
            #switch_category = sCategory_form.save(commit=False)
            switch_category_name = sCategory_form.save(commit=False)

            #switch_category.save()
            switch_category = Category.objects.filter(name = switch_category_name)[0]

    else:
        sCategory_form = SwitchCategoryForm()

    taskstemp = Task.objects.filter(category = switch_category)
    tasks = taskstemp.filter(user = request.user)


    return render(
        request,
        "taskManager.html",
        {
            'currentUser': request.user,
            'categories': categories,
            'tasks': tasks,
            'chosenCategory': switch_category,
            'form': sCategory_form,
        }
    )

#switch the category and show all tasks within selected category
def switchCategory(request, cat):
    #get all of the current user's categories for selected category
    categories = Category.objects.filter(user = request.user)
    category = categories.filter(name = cat)
    category = category[0]

    taskstemp = Task.objects.filter(category = category)
    tasks = taskstemp.filter(user = request.user)

    if request.method == 'GET':
        sCategory_form = SwitchCategoryForm(data = request.GET)
        if sCategory_form.is_valid():
            #create category object
            switch_category = sCategory_form.save(commit=False)
            #switch_category.save()
    else:
        sCategory_form = SwitchCategoryForm()


    return render(
        request,
        "taskManager.html",
        {
            'currentUser': request.user,
            'categories': categories,
            'tasks': tasks,
            'chosenCategory': category,
            'form': sCategory_form,
            'switched': switch_category,
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