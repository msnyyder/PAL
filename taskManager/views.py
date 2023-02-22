from django.shortcuts import render

# Create your views here.
def taskPage(request):
    return render(
        request, 
        "taskManager/taskPage.html", 
        {
            'currentUser':request.user,
        }
    )