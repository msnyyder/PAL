from django.shortcuts import render
from .models import *
from .forms import *
from datetime import datetime
import time
import json

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .agora_key.RtcTokenBuilder import RtcTokenBuilder
import random



def lobby(request):
    return render(request, 'lobby.html')

def room(request):
    return render(request, 'room.html')


def getToken(request):
    appId = "20314f62eba145a6a59267e867edb8c0"
    appCertificate = "e5dc4ec5b39845b9b8569f00ebddedeb"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    if member != None:
        member.delete()
    return JsonResponse('Member deleted', safe=False)

# Create your views here.
def taskPage(request):
    #initial variables
    categories = None
    tasks = None
    switch_category = None
    sCategory_form = None
    listOfDays = None
    task_days = None

    #making the task calendar
    #values for the current date
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    amountOfDays = getDays(currentMonth, currentYear)

    #get first day of the week (weekday) for calendar
    firstDate = datetime(currentYear, currentMonth, 1)
    startWeekDay = firstDate.weekday()

    #see if user is actually logged in 
    if request.user.id != None:
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
            sCategory_form = SwitchCategoryForm(request.user, data = request.POST)
            if sCategory_form.is_valid():
                #create category object
                #switch_category = sCategory_form.save(commit=False)
                oneName = sCategory_form.cleaned_data['allCategories']
                #switch_category.save()
                switch_category = Category.objects.filter(name = oneName, user = request.user)[0]

        else:
            sCategory_form = SwitchCategoryForm(request.user)

        #list of all tasks
        taskstemp = Task.objects.filter(category = switch_category)
        tasks = taskstemp.filter(user = request.user)

        #list of all the enddates for every task
        listOfDays = tasks.values('endDate')
        task_days_dateTime = tasks.filter(endDate__month__gte = currentMonth)
        #task_days = task_days_dateTime
        task_days = [None] * task_days_dateTime.count()
        task_array = [None] * task_days_dateTime.count()
        cnt = 0
        for day in task_days_dateTime:
            task_days[cnt] = day.endDate.date().day
            task_array[cnt] = day
            cnt = cnt + 1


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
            'taskDaysDateTime': task_array,
            'auth' : True
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