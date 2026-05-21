from django.db import models
from accounts.models import CustomUser


class BugReport(models.Model):
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('assigned',    'Assigned'),
        ('in_progress', 'In Progress'),
        ('fixed',       'Fixed'),
        ('reopened',    'Reopened'),
        ('closed',      'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('low',      'Low'),
        ('medium',   'Medium'),
        ('high',     'High'),
        ('critical', 'Critical'),
    ]
    LANGUAGE_CHOICES = [
        ('python',     'Python'),
        ('javascript', 'JavaScript'),
        ('java',       'Java'),
        ('cpp',        'C++'),
        ('csharp',     'C#'),
        ('c',          'C'),
        ('html',       'HTML'),
        ('css',        'CSS'),
        ('sql',        'SQL'),
        ('php',        'PHP'),
        ('go',         'Go'),
        ('rust',       'Rust'),
        ('other',      'Other'),
    ]
    ERROR_TYPE_CHOICES = [
        ('syntax',  'Syntax Error'),
        ('runtime', 'Runtime Error'),
        ('logic',   'Logic Error'),
        ('other',   'Other'),
    ]
    TIME_ESTIMATE_CHOICES = [
        ('2h',  '2 Hours'),
        ('4h',  '4 Hours'),
        ('6h',  '6 Hours'),
        ('10h', '10 Hours'),
        ('12h', '12 Hours'),
        ('1d',  '1 Day'),
        ('2d',  '2+ Days'),
    ]

    title           = models.CharField(max_length=200)
    description     = models.TextField()
    code_snippet    = models.TextField(blank=True)
    language        = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    error_type      = models.CharField(max_length=20, choices=ERROR_TYPE_CHOICES, default='other')
    priority        = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message   = models.TextField(blank=True)
    error_line      = models.CharField(max_length=20, blank=True, help_text="Line number of the error")
    fixed_code      = models.TextField(blank=True)
    fix_explanation = models.TextField(blank=True)
    time_estimate   = models.CharField(max_length=10, choices=TIME_ESTIMATE_CHOICES, blank=True)

    # file uploads
    attachment      = models.FileField(upload_to='bug_attachments/', blank=True, null=True)
    screenshot      = models.ImageField(upload_to='bug_screenshots/', blank=True, null=True)

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


class Comment(models.Model):
    bug       = models.ForeignKey(BugReport, on_delete=models.CASCADE, related_name='comments')
    author    = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content   = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on Bug #{self.bug.id}"


class Notification(models.Model):
    recipient  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message    = models.CharField(max_length=300)
    bug        = models.ForeignKey(BugReport, on_delete=models.CASCADE, null=True, blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notif → {self.recipient.username}: {self.message[:40]}"


class DeveloperRating(models.Model):
    developer  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    rated_by   = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_ratings')
    bug        = models.ForeignKey(BugReport, on_delete=models.CASCADE, null=True, blank=True)
    stars      = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review     = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('developer', 'rated_by', 'bug')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rated_by} rated {self.developer} → {self.stars}★"


class Feedback(models.Model):
    RATING_CHOICES  = [(i, str(i)) for i in range(1, 6)]
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('bug',     'Bug Report'),
        ('feature', 'Feature Request'),
    ]

    submitted_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='feedbacks'
    )
    category   = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    rating     = models.IntegerField(choices=RATING_CHOICES)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public  = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback by {self.submitted_by} — {self.rating}★"