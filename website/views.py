from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import bookingForm, loginForm, createUserForm, userSettingsForm
from .models import Booking

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')

def calculator(request):
    return render(request, 'pages/carbon-footprint.html')

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
def booking(request):
    form = bookingForm()
    if request.method == "POST":
        form = bookingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            if Booking.objects.filter(date=date).count() < 5:
                booking = Booking(
                    user=request.user,
                    type=form.cleaned_data['type'],
                    date=date,
                    notes=form.cleaned_data['notes'],
                    address=form.cleaned_data['address']
                )
                booking.save()
                messages.success(request, 'Your booking has been submitted successfully!')
                return redirect('my_bookings')
            else:
                messages.warning(request, 'This date is fully booked. Please choose another date.')
        else:
            messages.error(request, 'There was an error with your booking. Please try again.')
    
    context = {'form': form}
    return render(request, 'pages/booking.html', context=context)

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

@login_required(login_url="login")
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    context = {'bookings': bookings}
    return render(request, 'pages/my_bookings.html', context=context)

