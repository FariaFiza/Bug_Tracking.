from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import CustomUser
from bugs.models import BugReport, Notification


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
            messages.error(request, 'Please fix the errors below.')
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
            if not user.is_approved:
                messages.error(request, 'Your account has been banned. Contact admin.')
                return redirect('login')
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('bug_list')
        else:
            messages.error(request, 'Invalid username or password.')
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
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)

    if user.is_developer():
        my_bugs = BugReport.objects.filter(assigned_developer=user).order_by('-created_at')
        resolved = my_bugs.filter(status='fixed').count()
        pending  = my_bugs.exclude(status__in=['fixed','closed']).count()
    else:
        my_bugs  = BugReport.objects.filter(submitted_by=user).order_by('-created_at')
        resolved = my_bugs.filter(status='fixed').count()
        pending  = my_bugs.filter(status='pending').count()

    notifications = Notification.objects.filter(recipient=user, is_read=False)[:5]

    return render(request, 'accounts/profile.html', {
        'profile_user': user,
        'my_bugs':      my_bugs,
        'resolved':     resolved,
        'pending':      pending,
        'form':         form,
        'notifications': notifications,
    })


def developer_list(request):
    developers = CustomUser.objects.filter(role='developer', is_approved=True).order_by('-total_rating')
    return render(request, 'accounts/developer_list.html', {'developers': developers})


@login_required
def mark_notification_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('profile')


@login_required
def dashboard_view(request):
    user = request.user
    if user.is_admin_user():
        context = {
            'total_users':  CustomUser.objects.count(),
            'total_devs':   CustomUser.objects.filter(role='developer').count(),
            'total_bugs':   BugReport.objects.count(),
            'open_bugs':    BugReport.objects.filter(status='pending').count(),
            'fixed_bugs':   BugReport.objects.filter(status='fixed').count(),
            'recent_bugs':  BugReport.objects.select_related('submitted_by','assigned_developer').order_by('-created_at')[:10],
            'all_users':    CustomUser.objects.all().order_by('-date_joined')[:10],
        }
        return render(request, 'accounts/admin_dashboard.html', context)
    elif user.is_developer():
        assigned  = BugReport.objects.filter(assigned_developer=user)
        context = {
            'assigned_bugs':   assigned.count(),
            'completed_bugs':  assigned.filter(status='fixed').count(),
            'pending_bugs':    assigned.filter(status__in=['assigned','in_progress']).count(),
            'avg_rating':      user.avg_rating(),
            'rating_count':    user.rating_count,
            'recent_bugs':     assigned.order_by('-created_at')[:8],
        }
        return render(request, 'accounts/dev_dashboard.html', context)
    else:
        submitted = BugReport.objects.filter(submitted_by=user)
        context = {
            'submitted_bugs':  submitted.count(),
            'resolved_bugs':   submitted.filter(status='fixed').count(),
            'pending_bugs':    submitted.filter(status='pending').count(),
            'recent_bugs':     submitted.order_by('-created_at')[:8],
        }
        return render(request, 'accounts/user_dashboard.html', context)