from django import forms
from .models import BugReport, Comment, Feedback
from accounts.models import CustomUser


class BugReportForm(forms.ModelForm):
    assigned_developer = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='developer'),
        empty_label="-- Select a Developer --",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = BugReport
        fields = ['title', 'description', 'code_snippet', 'language', 'priority', 'error_message', 'assigned_developer', 'scheduled_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short, descriptive title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the bug...'}),
            'code_snippet': forms.Textarea(attrs={'class': 'form-control code-input', 'rows': 10, 'placeholder': '# Paste your buggy code here...'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'error_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Paste the error message/traceback...'}),
            # Added datetime-local widget to display interactive browser calendar-clock
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


class BugFixForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['status', 'fixed_code', 'fix_explanation']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'fixed_code': forms.Textarea(attrs={'class': 'form-control code-input', 'rows': 10, 'placeholder': '# Fixed code here...'}),
            'fix_explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Explain what was wrong and how you fixed it...'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment...'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['category', 'rating', 'message', 'is_public']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your thoughts...'}),
        }