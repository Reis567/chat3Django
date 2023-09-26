from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
from PIL import Image

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'photo', 'description']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            image = Image.open(photo)
            if image.width < 500 or image.height < 500:
                raise ValidationError("A imagem de perfil deve ter no mínimo 500x500 pixels.")
        return photo

    def clean_banner(self):
        banner = self.cleaned_data.get('banner')
        if banner:
            image = Image.open(banner)
            if image.width < 1000 or image.height < 200:
                raise ValidationError("O banner deve ter no mínimo 1000x200 pixels.")
        return banner
    
    def save(self, commit=True):
            user_profile = super().save(commit=False)

            # Redimensiona a imagem do banner para 1000x200 pixels
            if user_profile.banner:
                banner_image = Image.open(user_profile.banner)
                banner_image = banner_image.resize((1000, 200), Image.ANTIALIAS)
                banner_image.save(user_profile.banner.path)

            # Redimensiona a imagem de perfil para 500x500 pixels
            if user_profile.photo:
                profile_image = Image.open(user_profile.photo)
                profile_image = profile_image.resize((500, 500), Image.ANTIALIAS)
                profile_image.save(user_profile.photo.path)

            if commit:
                user_profile.save()

            return user_profile