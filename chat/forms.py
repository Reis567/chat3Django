from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
from PIL import Image

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email','photo','banner', 'description']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            image = Image.open(photo)
            if image.width < 500 or image.height < 500:
                raise ValidationError("A imagem de perfil deve ter no mínimo 500x500 pixels.")
            if not photo.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise ValidationError("Formato de imagem não suportado. Use JPG, JPEG, PNG ou GIF.")
        return photo

    def clean_banner(self):
        banner = self.cleaned_data.get('banner')
        if banner:
            image = Image.open(banner)
            if image.width < 1000 or image.height < 200:
                raise ValidationError("O banner deve ter no mínimo 1000x200 pixels.")
            if not banner.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise ValidationError("Formato de imagem não suportado. Use JPG, JPEG, PNG ou GIF.")
        return banner
    
    def save(self, commit=True):
        user_profile = super().save(commit=False)

        # Redimensiona a imagem do banner para 1000x200 pixels
        if user_profile.banner:
            banner_image = Image.open(user_profile.banner)
            novo_tamanho=(1000,200)
            banner_image = banner_image.resize(novo_tamanho)
            print(f'banner size :{banner_image.size}')
            banner_image.save(user_profile.banner.path)

        # Redimensiona a imagem de perfil para 500x500 pixels
        if user_profile.photo:
            profile_image = Image.open(user_profile.photo)
            novo_tamanho=(180,180)
            profile_image = profile_image.resize(novo_tamanho)
            print(f'photo size :{profile_image.size}' )
            profile_image.save(user_profile.photo.path)

        if commit:
            user_profile.save()

        return user_profile