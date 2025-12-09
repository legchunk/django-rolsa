from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import loginForm, createUserForm, userSettingsForm

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')

def calculator(request):
    return render(request, 'pages/carbon-footprint.html')


def booking(request):
    return render(request, 'pages/booking.html')

def about(request):
    return render(request, 'pages/about.html')

def register(request):
    form = createUserForm()

    if request.method == "POST":
        form = createUserForm(request.POST)            
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'pages/register.html', context=context)


def login(request):
    form = loginForm()

    if request.method == "POST":
        form = loginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid username or password')

    context = {"form": form}
    return render(request, 'pages/login.html', context=context)

@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def settings(request):
    if request.method == "POST":
        form = userSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your details have been updated successfully!')
            return redirect('settings')
    else:
        form = userSettingsForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'pages/settings.html', context=context)

