from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_update, name='profile_update'),
    path('events/', views.events, name='events'),
    path('events/new/', views.event_create, name='event_create'),
    path('friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
]
