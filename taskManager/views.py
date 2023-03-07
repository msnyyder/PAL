from django.shortcuts import render


# Create your views here.
def taskPage(request):
    return render(
        request,
        "homepage.html",
        {
            'currentUser': request.user,
        }
    )
