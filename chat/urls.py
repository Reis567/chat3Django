from django.urls import path
from .views import home,rooms,room

urlpatterns = [
    path('' , home , name='home'),
    path('rooms/', rooms, name='rooms'),
    path('room/<str:slug>/',room, name='room'),
    ]
