from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Post, Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image'] 
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 mt-1 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500',
            'placeholder': 'Enter your email'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 mt-1 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500',
            'placeholder': 'Enter your password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 mt-1 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500',
            'placeholder': 'Re-enter your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-3 mt-1 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500',
                'placeholder': 'Enter your username'
            })
        }