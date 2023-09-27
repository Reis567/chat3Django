from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room,Message,UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserProfileForm
from django.db import IntegrityError


class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuário ou senha incorretos.')
        return super().form_invalid(form)


@login_required
def custom_logout(request):
    # Realiza o logout do usuário
    LogoutView.as_view()(request) 

    return render(request, 'user/logout.html')  

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)  # Autentica o usuário recém-criado
            messages.success(request, f'Conta criada para {username}! Você está agora logado.')
            return redirect('home')  # Redireciona para a página inicial ou qualquer outra página desejada após o registro bem-sucedido
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
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
        user_profile = UserProfile.objects.get(user=request.user)
        username = user_profile.user.username
    except Room.DoesNotExist:
        # Lidar com o caso em que a sala não existe
        return HttpResponse("A sala não existe.", status=404)
    
    return render(request, 
                  "room.html",
            {
                "room_name":room_name,
                "slug":slug,
                'messages':messages,
                'user_name':username,
                'user_profile':user_profile})

@login_required
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    return render(request, 'profile_temps/profile.html', {'user_profile': user_profile})

@login_required
def edit_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Lidar com o caso em que o perfil do usuário não existe
        messages.error(request, 'Seu perfil de usuário não existe.')
        return redirect('home')  # Redirecionar para a página inicial ou outra página apropriada
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        try:
            if form.is_valid():
                user_profile.user = request.user
                form.save()
                messages.success(request, 'Perfil atualizado com sucesso.')
                return redirect('edit_user_profile')
            else:
                messages.error(request, 'Por favor, corrija os erros no formulário.')
        except Exception as e:
            messages.error(request, f'Erro ao salvar perfil: {str(e)}')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request,
                  'profile_temps/edit_profile.html',
                  {
                    'form': form,
                    'user_profile': user_profile
                })
