from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room





# Create your views here.

# View de login personalizada
class CustomLoginView(LoginView):
    template_name = 'user/login.html'  


def custom_logout(request):
    # Realiza o logout do usuário
    LogoutView.as_view()(request) 

    return render(request, 'user/logout.html')  

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Agora você pode fazer login.')
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})




def home(request):
    return render(request ,'home.html')


def rooms(request):
    rooms = Room.objects.all().order_by('-pk')
    return render(request, 'rooms.html' ,{
        'rooms':rooms
    })


def room(request, slug):
    try:
        room = Room.objects.get(slug=slug)
    except Room.DoesNotExist:
        # Lidar com o caso em que a sala não existe
        return HttpResponse("A sala não existe.", status=404)
    
    return render(request, 'room.html', {
        'room': room
    })