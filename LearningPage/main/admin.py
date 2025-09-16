from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Uzytkownik)
admin.site.register(models.Wpis)
admin.site.register(models.User_Wpis)
