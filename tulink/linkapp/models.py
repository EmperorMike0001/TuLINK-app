from django.contrib.auth.models import AbstractUser
from django.db import models
from geopy.distance import geodesic


class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions', blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    visibility = models.BooleanField(default=True)  # Determines if the profile is visible to others
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def distance_to(self, other_profile):
        return geodesic((self.latitude, self.longitude), (other_profile.latitude, other_profile.longitude)).km


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')  # statuses: pending, accepted, rejected

