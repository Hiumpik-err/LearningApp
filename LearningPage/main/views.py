from django.shortcuts import render, redirect
from .models import Uzytkownik
from django.contrib.auth import login
from django.contrib import messages

def login(request):
    if request.method == "POST":
        if "registering" in request.POST:
            email_input = request.POST.get("input-username")
            password_input = request.POST.get("input-password")
            password2_input = request.POST.get("input-repeat-password")
            print(email_input)
            print(password_input)
            print(password2_input)
            

            if(not email_input or not password_input or not password2_input):
                messages.error(request, "Fill all fields")
                return redirect("login")

            if(password_input != password2_input): 
                messages.error(request, "Passwords dont match")
                return redirect("login")

            login(request, user)
            user = Uzytkownik.objects.create_user(email = email_input, password = password_input)
            print(f"Utworzono uzytkownika o email = {email_input} i hasle ={password_input}")
            
            return redirect("home")
            
    return render(request, "login.html")

def home(request):

    return render(request, "home.html")

def item_view(request):

    return render(request, "item_view.html")

def create_item(request, type):
    context = {"type" : type}
    return render(request, "create_item.html", context)

def available_article(request):
    return render(request, "articles.html")

def available_courses(request):
    return render(request, "courses.html")

def available_quizzes(request):
    return render(request, "quizzes.html")

def search_item(request):
    pass