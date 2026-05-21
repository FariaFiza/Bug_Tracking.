from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[('user', 'Normal User'), ('developer', 'Developer')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}))

    class Meta:
        model = CustomUser
        # password1, password2 এখান থেকে বাদ দেওয়া হয়েছে
        fields = ['username', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # পাসওয়ার্ড ফিল্ডের ডিজাইন ঠিক রাখার জন্য উইজেট আপডেট
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'class' : 'form-control','placeholder':'Create password'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'class' : 'form-control','placeholder':'Confirm password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This Email is already registered")
        return email

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder': 'Enter your username'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control', 'placeholder': 'Enter your password'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [ 'email', 'bio','skills','availability']
        widgets = {
             'email': forms.EmailInput(attrs={'class': 'form-control'}),
             'bio': forms.Textarea(attrs={'class': 'form-control','rows':3,'placeholder':'Tell us your yourself...'}),
             'skills': forms.TextInput(attrs={'class': 'form-control','placeholder':'e.g. Python,Java'}),
              'availability': forms.Select(attrs={'class': 'form-control'}),
        }