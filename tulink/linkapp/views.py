from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileUpdateForm, EventForm
from .models import User, Profile, Event, Friendship
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def home(request):
    return render(request, 'base.html')

def login_view(request):
    next_page = request.GET.get('next', 'profile')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in!')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Form is not valid. Please check your input and try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error occurred while creating your account. Please try again.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    user_profile = request.user.profile
    return render(request, 'profile.html', {'profile': user_profile})

@login_required
def profile_update(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating your profile. Please try again.')
    else:
        form = ProfileUpdateForm(instance=user_profile)
    return render(request, 'profile_update.html', {'form': form})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events')
        else:
            messages.error(request, 'Error creating event. Please check your input and try again.')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

@login_required
def send_friend_request(request, user_id):
    user = User.objects.get(id=user_id)
    friendship = Friendship.objects.create(user=request.user, friend=user, status='pending')
    messages.success(request, 'Friend request sent successfully!')
    return redirect('profile')

def events(request):
    events_list = Event.objects.all()
    return render(request, 'events.html', {'events': events_list})
