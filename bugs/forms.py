from django import forms
from .models import BugReport, Comment, Feedback,DeveloperRating
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
        fields = ['title', 'description', 'language', 'error_type','priority','code_snippet', 'error_message', 'error_line','attachment','screenshot','assigned_developer']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short, clear bug title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe what went wrong...'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'error_type': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'code_snippet': forms.Textarea(attrs={'class': 'form-control code-input', 'rows': 10,'placeholder': '# Paste your buggy code here...'}),
            'error_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Paste the error message/traceback...'}),
            'error_line':forms.TextInput(attrs={'class': 'form-control','placeholder':'e.g. 42'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'screenshot': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }


class BugFixForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['status','time_estimate', 'fixed_code', 'fix_explanation']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'time_estimate': forms.Select(attrs={'class': 'form-control'}),
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
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your thoughts about BugHive...'}),
        }

class DeveloperRatingForm(forms.ModelForm):
    class Meta:
        model = DeveloperRating
        fields = ['stars', 'review']
        widgets = {
            'stars': forms.Select(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control','rows': 3, 'placeholder': 'Write a review for this developer...'}),


        }








