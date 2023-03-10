from django.shortcuts import render


# Create your views here.
def taskPage(request):
    return render(
        request,
        "taskManager.html",
        {
            'currentUser': request.user,
        }
    )
