from .models import Uzytkownik, Wpis, User_Wpis
from django.forms import ModelForm

class WpisForm(ModelForm):
    class Meta:
        model = Wpis
        fields = ["title", "subject", "category"]