from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Event


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'latitude', 'longitude', 'visibility']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'location']
