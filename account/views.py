from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
from account.models import Profile


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        exist = User.objects.filter(username=username).first()
        if password != confirm_password:
            messages.error(request, 'Password unmatched')
            return redirect('home')
        if exist:
            messages.error(request, 'Username already exists')
            return redirect('home')
        exist = User.objects.filter(email=email).first()
        if exist:
            messages.error(request, 'Email already exists')
            return redirect('home')
        User.objects.create_user(username=username, password=password, email=email)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            Profile.objects.create(user=user)
            messages.success(request, 'Account created successful')
            return redirect('home')
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
        else:
            messages.error(request, 'Username and password unmatched')
            return redirect('home')
    return redirect('home')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('home')


