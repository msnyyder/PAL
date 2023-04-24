from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from datetime import date
from .models import *
from taskManager.models import *
from .forms import *
import os
import time

import PALAPP

from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
import os

import PALAPP
import pandas as pd
import numpy as np

class Schedule:
    def __init__(self, ACT, MPE, taken):
        self.ACT = ACT
        self.MPE = MPE
        self.hour_limit = 19
        self.taken = taken
        self.data = pd.read_csv('.\\course_data_2017_cleaner.csv')
        self.data.dropna(subset=['CRN', 'Title', 'Crse'], inplace=True)
        self.data = self.data[self.data["Crse"].str.isnumeric()]
        self.NUM_COLLONADES = 9

        self.constraints = {
            'COMM' : [],
            'STAT' : ['M136', 'M142'],
            'C146' : [], 
            'C157': [],
            'C170' : ['MPEX', 'M115', 'M116'],
            'C175' : [],
            'C180' : ['C170', '_ACT', 'M116', 'M123'],
            'C221' : ['_ACT', 'M117', 'M118', 'M136', 'M137', 'C180'], 
            'C239' : ['M117', 'M118', 'M136', 'M137', 'M237', 'M331'], 
            'C245' : ['C146'], 
            'C250' : ['C180'],
            'C257' : ['C257'],
            'C270' : ['C180'],
            'C290' : ['C180', 'M117', 'M118', 'M136', 'M137'],
            'C295' : [],
            'C299' : ['C180|C221'],
            'C301' : ['C146', 'C170', 'C180', 'C239'],
            'C315' : ['C290'],
            'C325' : ['C290'],
            'C331' : ['C290'],
            'C339' : ['C290|M136'],
            'C351' : ['C290'],
            'C360' : ['C331|C351', 'C239', 'C180', 'COMM'],
            'C369' : [],
            'C370' : [],
            'C372' : ['C290'],
            'C381' : ['C290'],
            'C382' : ['C221', 'C290'],
            'C389' : ['C351'],
            'C396' : ['C351|C331|COMM|ENGL'],
            'C405' : ['M137|M300|C180', 'M137|M300|C146'],
            'C406' : ['M307|M327|M331|C405'],
            'C421' : ['C339|C331|STAT'],
            'C425' : ['C325|C382'],
            'C443' : ['C331|C351'],
            'C445' : ['C425'],
            'C446' : ['M307|C331'],
            'C450' : ['C325|C381'],
            'C456' : ['C331|C339'],
            'C473' : ['M307|M310'],
            'C475' : [],
            'C476' : ['C360'],
            'C496' : ['C360|C396']
        }

        self.reqs = [
            'STAT',
            'C180', 
            'C290',
            'C331',
            'C325',
            'C339',
            'C351',
            'C360',
            'C382',
            'C396',
            'C421',
            'C425',
            'C496'
            ]
        
    def req_satisfied(self, condition, satisfied):
        if condition == '_ACT':
            return self.ACT
        elif condition == 'MPEX':
            return self.MPE
        else:
            return condition in satisfied

    def get_hours(self, course):
        if course in ['C180', 'C290']:
            return 4
        return 3
    
    def min_to_take(self, req, satisfied):
        if req[0] != 'C' or len(self.constraints[req]) == 0:
            return [req]

        min = [None] * 100
        for prereq in self.constraints[req]:
            to_take = []
            for indiv in prereq.split('|'):
                if not self.req_satisfied(indiv, satisfied) and indiv not in ['MPEX', '_ACT']:
                    to_take.extend(self.min_to_take(indiv, satisfied))
                elif indiv in ['MPEX', '_ACT']:
                    to_take = min = [None] * 100 
                    break
            to_take = to_take + [req]
            if len(to_take) < len(min):
                min = to_take
        return min
    
    def gen_paths(self, taken):
        in_schedule = []
        for req in self.reqs:
            if req not in taken:
                in_schedule.extend(self.min_to_take(req, taken + in_schedule))
        return in_schedule
    
    def eligible(self, course, credits_recieved):
        if course[0] != 'C' or len(self.constraints[course]) == 0:
            return True
        
        conditions = self.constraints[course]
        for condition in conditions:
            if all([self.req_satisfied(prereq, credits_recieved) for prereq in condition.split('|')]):
                return True

        return False
    
    def find_courses_after(self, course, afteryear, curterm):
        if course[0] == 'C' and course != 'COMM':
            return self.data.loc[((self.data['Crse'].astype('int32') == int(course[-3:])) & (self.data['Year'] >= afteryear) & ((self.data['Term'] == 'Spring') | (curterm == 'Fall')))]
        return []
     
    def find_courses_in(self, course, curyear, curterm):
        if course[0] == 'C' and course != 'COMM':
            return self.data.loc[((self.data['Crse'].astype('int32') == int(course[-3:])) & (self.data['Year'] == curyear) & (self.data['Term'] == curterm))]
        return []
    
    def schedule(self):
        main_schedule = self.gen_paths(self.taken)
        taken_so_far = []
        collonades = taken_so_far.count('COLL')

        [Y, M, D] = [int(val) for val in str(date.today()).split('-')]

        term = 'Fall' if M < 8 else 'Spring'
        year = Y if M < 8 else Y + 1

        titles = []
        crns = []
        profs = []
        hours = []

        while len(main_schedule) > 0:

            num_hours = 0
            can_take = [req for req in main_schedule if self.eligible(req, self.taken + taken_so_far)]
            for course in can_take:
                if num_hours + self.get_hours(course) > self.hour_limit:
                    continue
                courses = self.find_courses_in(course, year, term)
                #print(courses)
                all_left = self.find_courses_after(course, year, term)
                if len(courses) > 0:
                    for idx, row in courses.iterrows():
                        titles.append(row['Title'])
                        crns.append(row['CRN'])
                        profs.append(row['Instructor'])
                        hours.append(row['Cred'])
                elif len(all_left) == 0:
                    titles.append(course)
                    crns.append('')
                    profs.append('')
                    hours.append(self.get_hours(course))
                else:
                    continue

                num_hours += self.get_hours(course)
                taken_so_far.append(course)
                main_schedule.remove(course)
            
            while collonades < self.NUM_COLLONADES and num_hours + self.get_hours('COLL') < self.hour_limit:
                titles.append('COLL')
                crns.append('')
                profs.append('')
                hours.append(3)
                taken_so_far.append('COLL')
                num_hours += self.get_hours('COLL')
                collonades += 1

            if term == 'Fall':
                term = 'Spring'
            else:
                term = 'Fall'
                year += 1
        
        return titles, crns, profs, hours

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
    currentUser = request.user
    currentUserEx = UserExtended.objects.filter(user = request.user)

    coursesTaken = ""
    new_added_course = None
    existsVal = True
    form = None
    isAdvisor = False

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
            'fullName': currentUser.get_full_name(),
            'coursesTaken': coursesTaken,
            'existingCourseForm': form,
            'new_added_course': new_added_course,
            'existsVal': existsVal,
            'isAdvisor': isAdvisor,
        }
    )

def schedule(request):
    return redirect(courseRegister)

def courseRegister(request):
    schedule = Schedule(False, False, list(CourseTaken.objects.filter(user=request.user).values_list('course', flat=True)))
    titles, crns, profs, hours = schedule.schedule()
    #print(schedule.data.dtypes)
    code = ''
    code += '<tbody>\n'
    for idx in range(len(titles)):
        code += f'<tr class="text-start">\n'
        code += f'<td>{titles[idx]}</td>\n'
        code += f'<td>{crns[idx]}</td>\n'
        code += f'<td>{profs[idx]}</td>\n'
        code += f'<td>{hours[idx]}</td>\n</tr>\n'
        
    code += '\n</tbody>\n'
    #print(code)

    return render(
        request, 
        "courseRegistration/schedulerFinal.html",
        {
            'currentUser':request.user,
            'taken' : CourseTaken.objects.filter(user=request.user),
            'code' : code,
            'addCourseForm' : ModifyCourse(),
            'registerForm' : RegisterForm(),
        }
    )

def addCourse(request):
    if request.method == 'POST':
        courseForm = ModifyCourse(data = request.POST)
        if courseForm.is_valid():
            data = courseForm.cleaned_data
            modCourse = data['course'].upper()
            if data['addStatus'] == 'add':
                if modCourse == 'COLL' or CourseTaken.objects.filter(user=request.user).filter(course=modCourse).count() == 0:
                    CourseTaken.objects.create(
                        user=request.user,
                        course=modCourse
                    )
            else:
                toDelete = CourseTaken.objects.filter(user=request.user).filter(course=modCourse).first()
                if toDelete is not None:
                    toDelete.delete()
    return redirect(courseRegister)

def home(request):
    if request.user.is_authenticated:
        #list of all tasks
        allTasks = Task.objects.filter(user = request.user)
        today = date.today()
        todaysTasks = allTasks.filter(endDate__year = today.year, endDate__month = today.month, endDate__day = today.day)
        return render(
            request, 
            "courseRegistration/home.html", 
            {
                'todaysTasks':todaysTasks,
            }
        )
    else:
        return render(
            request, 
            "courseRegistration/home.html", 
            {
                'todaysTasks':None,
            }
        )