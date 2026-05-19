from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import CustomUser


def register_view(request):
    if request.user.is_authenticated:
        return redirect('bug_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Account created successfully.')
            return redirect('bug_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('bug_list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('bug_list')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    from bugs.models import BugReport
    if user.is_developer():
        my_bugs = BugReport.objects.filter(assigned_developer=user).order_by('-created_at')
    else:
        my_bugs = BugReport.objects.filter(submitted_by=user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {'profile_user': user, 'my_bugs': my_bugs})


def developer_list(request):
    developers = CustomUser.objects.filter(role='developer')
    return render(request, 'accounts/developer_list.html', {'developers': developers})