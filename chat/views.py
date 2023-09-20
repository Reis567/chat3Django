from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room,Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required



class CustomLoginView(LoginView):
    template_name = 'user/login.html'  


@login_required
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


@login_required
def rooms(request):
    room_list = Room.objects.all().order_by('-pk')
    
    items_per_page = 6
    paginator = Paginator(room_list, items_per_page)
    
    page = request.GET.get('page')
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)
    
    return render(request, 'rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    try:
        room_name = Room.objects.get(slug=slug).name
        messages = Message.objects.filter(room=Room.objects.get(slug=slug))
    except Room.DoesNotExist:
        # Lidar com o caso em que a sala não existe
        return HttpResponse("A sala não existe.", status=404)
    
    return render(request, 
                  "room.html",
            {
                "room_name":room_name,
                "slug":slug,
                'messages':messages})

    
    