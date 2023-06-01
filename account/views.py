from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, 
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, 
                                       data=request.POST,
                                       files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request,
                  'account/edit_profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
        




def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            
            new_user.set_password(
                user_form.cleaned_data['password'])
            
            new_user.save()
            
            #creating users profile
            Profile.objects.create(user=new_user)
            
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
            
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',
                  {'user_form': user_form})
        
        
        
        
        
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
                  {'section': 'dashboard'})