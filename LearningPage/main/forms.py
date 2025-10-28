# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Uzytkownik

class UzytkownikCreationForm(UserCreationForm):
    class Meta:
        model = Uzytkownik
        fields = ('email',) 

class UzytkownikChangeForm(UserChangeForm):
    class Meta:
        model = Uzytkownik
        fields = ('email', 'is_active', 'is_admin')