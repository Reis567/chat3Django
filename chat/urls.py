from django.urls import path
from .views import home,rooms

urlpatterns = [
    path('' , home , name='home'),
    path('rooms/', rooms, name='rooms'),
]
