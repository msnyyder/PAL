from django.contrib.auth import login, logout
from django.contrib import messages
from datetime import date
from .models import *
from taskManager.models import *
from .forms import *
from .Objs import Schedule

from django.shortcuts import  render, redirect

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
            scheduleAs = ScheduleAs(user=user, scheduleAs=user)
            scheduleAs.save()

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
            'auth' : True
        }
    )

def schedule(request):
    if request.method == 'POST':
        scheduleForm = RegisterForm(request.user, data = request.POST)
        if scheduleForm.is_valid():
            data = scheduleForm.cleaned_data
        
            schedule = Schedule(data['ACT'], data['ACT'], list(CourseTaken.objects.filter(user=data['user']).values_list('course', flat=True)))
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
                    'registerForm' : RegisterForm(request.user),
                    'auth' : True
                }
            )

    return redirect(courseRegister)

def courseRegister(request, MPE=False, ACT=False):
    schedule = Schedule(ACT, MPE, list(CourseTaken.objects.filter(user=request.user).values_list('course', flat=True)))
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
            'registerForm' : RegisterForm(request.user),
            'auth' : True
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

def logout(request):
    logout(request)
    return redirect(home)

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
                'auth' : True
            }
        )
    else:
        return render(
            request, 
            "courseRegistration/home.html",
            {
                'todaysTasks':None,
                'auth' : False
            }
        )