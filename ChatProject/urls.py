from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from chat import views

urlpatterns = [
    path('admin/', admin.site.urls),

    ## User urls
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),


    ## Chat urls
    path('chat/', include('chat.urls')),
    path('' , views.home , name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('room/<str:slug>/',views.room, name='room'),
    path('profile/', views.user_profile, name='user_profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)