from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:                    
                    login(request, user)
                    return HttpResponse('Authenticated succesfully, you are now logged in')
                else:
                    return HttpResponse('Your account is inactive')
            else:
                return HttpResponse('Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 
                  'account/dashboard.html',
                  {'section': 'Dashboard'})