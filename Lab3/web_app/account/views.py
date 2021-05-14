from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.


def user_login(request):
    if request.method == "GET":
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is None:
                return HttpResponse('Invalid login')
            else:
                if user.is_active:
                    login(request, user)
                    return redirect("/admin/") 
                else:
                    return HttpResponse('Disabled account')
    
    return render(request, "account/login.html", {"form": form})
