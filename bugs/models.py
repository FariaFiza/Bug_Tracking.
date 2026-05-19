from django.db import models
from accounts.models import CustomUser


class BugReport(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('csharp', 'C#'),
        ('php', 'PHP'),
        ('ruby', 'Ruby'),
        ('go', 'Go'),
        ('rust', 'Rust'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    code_snippet = models.TextField(blank=True, help_text="Paste your buggy code here")
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    error_message = models.TextField(blank=True)
    fixed_code = models.TextField(blank=True, help_text="Developer's fixed version of the code")
    fix_explanation = models.TextField(blank=True, help_text="Developer's explanation of the fix")

    # New field for scheduling live help
    scheduled_time = models.DateTimeField(null=True, blank=True, help_text="Select a date and time for your session")

    # ForeignKey connections
    submitted_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='submitted_bugs', null=True, blank=True
    )
    assigned_developer = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL,
        related_name='assigned_bugs', null=True, blank=True,
        limit_choices_to={'role': 'developer'}
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.priority.upper()}] {self.title} — {self.status}"

    def get_status_color(self):
        colors = {
            'open': '#f59e0b',
            'in_progress': '#3b82f6',
            'resolved': '#10b981',
            'closed': '#6b7280',
        }
        return colors.get(self.status, '#6b7280')

    def get_priority_color(self):
        colors = {
            'low': '#10b981',
            'medium': '#f59e0b',
            'high': '#f97316',
            'critical': '#ef4444',
        }
        return colors.get(self.priority, '#6b7280')


class Comment(models.Model):
    bug = models.ForeignKey(BugReport, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on Bug #{self.bug.id}"


class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('developer', 'Developer Rating'),
    ]

    submitted_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='feedbacks'
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    rating = models.IntegerField(choices=RATING_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback by {self.submitted_by} — {self.rating}★"