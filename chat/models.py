from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    # Gera o caminho dinâmico baseado no nome de usuário e nome do arquivo
    return f'profile_photos/{instance.user.username}/{filename}'

class Room(models.Model):
    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=50)
    users = models.ManyToManyField(User)

    def get_user_count(self):
        return self.users.count()

    def __str__(self):
        return self.name  # Ou qualquer outra representação que você desejar

class Message(models.Model):

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'  # Retorna o nome do usuário e o conteúdo da mensagem


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

# Função para criar ou obter o UserProfile associado a um User
def get_or_create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

# Registrar o sinal para criar ou obter o UserProfile
post_save.connect(get_or_create_user_profile, sender=User)
