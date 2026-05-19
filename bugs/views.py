from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import BugReport, Comment, Feedback
from .forms import BugReportForm, BugFixForm, CommentForm, FeedbackForm
from accounts.models import CustomUser


def home(request):
    stats = {
        'total_bugs': BugReport.objects.count(),
        'open_bugs': BugReport.objects.filter(status='open').count(),
        'resolved_bugs': BugReport.objects.filter(status='resolved').count(),
        'total_devs': CustomUser.objects.filter(role='developer').count(),
    }
    recent_bugs = BugReport.objects.select_related('submitted_by', 'assigned_developer').order_by('-id')[:5]
    feedbacks = Feedback.objects.filter(is_public=True).select_related('submitted_by').order_by('-id')[:4]
    return render(request, 'bugs/home.html', {'stats': stats, 'recent_bugs': recent_bugs, 'feedbacks': feedbacks})


@login_required
def bug_list(request):
    bugs = BugReport.objects.select_related('submitted_by', 'assigned_developer')
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    language = request.GET.get('language', '')

    if q:
        bugs = bugs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if status:
        bugs = bugs.filter(status=status)
    if priority:
        bugs = bugs.filter(priority=priority)
    if language:
        bugs = bugs.filter(language=language)

    if request.user.is_developer and not any([q, status, priority, language]):
        bugs = bugs.filter(assigned_developer=request.user)

    return render(request, 'bugs/bug_list.html', {
        'bugs': bugs,
        'q': q, 'status': status, 'priority': priority, 'language': language,
    })


@login_required
def bug_create(request):
    # Enforce session limits: check if normal user has sessions remaining
    if request.user.role == 'user' and request.user.free_sessions_remaining <= 0:
        messages.error(request,
                       'You have used up all your free sessions. Please contact support or upgrade your account.')
        return redirect('home')

    if request.method == 'POST':
        form = BugReportForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.submitted_by = request.user
            bug.save()

            # Deduct a session token if the sender is a normal user
            if request.user.role == 'user':
                request.user.free_sessions_remaining -= 1
                request.user.save()
                messages.success(request,
                                 f'Session requested successfully! You have {request.user.free_sessions_remaining} free sessions left.')
            else:
                messages.success(request, 'Session requested successfully!')

            return redirect('bug_detail', pk=bug.pk)
    else:
        form = BugReportForm()
    return render(request, 'bugs/bug_form.html', {'form': form, 'title': 'Submit Bug Report'})


@login_required
def bug_detail(request, pk):
    bug = get_object_or_404(BugReport.objects.select_related('submitted_by', 'assigned_developer'), pk=pk)
    comments = bug.comments.select_related('author')
    comment_form = CommentForm()
    fix_form = None

    if request.user.is_developer or request.user.is_admin_user:
        fix_form = BugFixForm(instance=bug)

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.bug = bug
                comment.author = request.user
                comment.save()
                messages.success(request, 'Comment added!')
                return redirect('bug_detail', pk=pk)

        elif 'fix_submit' in request.POST and (request.user.is_developer or request.user.is_admin_user):
            fix_form = BugFixForm(request.POST, instance=bug)
            if fix_form.is_valid():
                fix_form.save()
                messages.success(request, 'Bug fix submitted!')
                return redirect('bug_detail', pk=pk)

    return render(request, 'bugs/bug_detail.html', {
        'bug': bug, 'comments': comments,
        'comment_form': comment_form, 'fix_form': fix_form,
    })


@login_required
def bug_edit(request, pk):
    bug = get_object_or_404(BugReport, pk=pk)
    if bug.submitted_by != request.user and not request.user.is_admin_user:
        messages.error(request, 'You can only edit your own bug reports.')
        return redirect('bug_detail', pk=pk)
    if request.method == 'POST':
        form = BugReportForm(request.POST, instance=bug)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bug report updated!')
            return redirect('bug_detail', pk=pk)
    else:
        form = BugReportForm(instance=bug)
    return render(request, 'bugs/bug_form.html', {'form': form, 'title': 'Edit Bug Report', 'bug': bug})


@login_required
def bug_delete(request, pk):
    bug = get_object_or_404(BugReport, pk=pk)
    if bug.submitted_by != request.user and not request.user.is_admin_user:
        messages.error(request, 'You can only delete your own bug reports.')
        return redirect('bug_detail', pk=pk)
    if request.method == 'POST':
        bug.delete()
        messages.success(request, 'Bug report deleted.')
        return redirect('bug_list')
    return render(request, 'bugs/bug_confirm_delete.html', {'bug': bug})


@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.submitted_by = request.user
            fb.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'bugs/feedback_form.html', {'form': form})


def feedback_list(request):
    feedbacks = Feedback.objects.filter(is_public=True).select_related('submitted_by')
    return render(request, 'bugs/feedback_list.html', {'feedbacks': feedbacks})