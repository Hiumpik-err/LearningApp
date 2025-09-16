from django.db import models
from django import forms

class Uzytkownik(models.Model):
    id_uzytkownika = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length= 50)
    fname = models.CharField(max_length= 20)
    lname = models.CharField(max_length=50)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return username

class Wpis(models.Model):
    id_wpisu = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 50)
    file_name = models.CharField(max_length = 30)
    subject = models.CharField(max_length = 30)
    category = models.CharField(max_length = 15)

    def __str__(self):
        return title

class User_Wpis(models.Model):
    id_uzytkownika = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    id_wpisu = models.ForeignKey(Wpis, on_delete= models.CASCADE)
    score = models.IntegerField(default = 0)
    data = models.DateField(auto_now_add = True)

