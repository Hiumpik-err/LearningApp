from django.shortcuts import render, redirect
from .models import Uzytkownik
from django.contrib.auth import login as auth_login, authenticate
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
                raise Exception("Not all requiered fields are filled")

            if(password_input != password2_input): 
                messages.error(request, "Passwords dont match")
                raise Exception("Passwords dont match")
            try:
                user = Uzytkownik.objects.create_user(email = email_input, password = password_input)
                print(f"Utworzono uzytkownika o email = {email_input} i hasle ={password_input}")
                auth_login(request, user=user)
                
                return redirect("home")
            except Exception as e:
                messages.info(request, f"Error: {e}")

        if "logging" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                user = authenticate(request, email=email, password=password)

                if not user:
                    messages.error(request, "User not found. womp womp ")
                    raise Exception("User not found")
                
                auth_login(request, user)
                return redirect("home")

            except Exception as e:
                    messages.error(request, f"Error: {e}")
                    print(e)
                    return redirect("login")
                

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