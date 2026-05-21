from django.contrib import admin
from .models import BugReport, Comment, Feedback


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'submitted_by', 'assigned_developer', 'priority', 'status', 'language', 'created_at']
    list_filter = ['status', 'priority', 'language']
    search_fields = ['title', 'description']
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'bug', 'created_at']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['submitted_by', 'category', 'rating', 'is_public', 'created_at']
    list_filter = ['category', 'rating', 'is_public']