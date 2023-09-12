from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages




# Create your views here.

def home(request):
    return render(request ,'home.html')

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