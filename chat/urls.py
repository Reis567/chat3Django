from django.urls import path
from .views import home,rooms,room,user_profile,edit_user_profile

urlpatterns = [
    path('' , home , name='home'),
    path('rooms/', rooms, name='rooms'),
    path('room/<str:slug>/',room, name='room'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/edit/', edit_user_profile, name='edit_user_profile'),
    ]
