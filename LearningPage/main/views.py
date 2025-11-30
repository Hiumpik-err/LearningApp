from django.shortcuts import render, redirect
from .models import Uzytkownik, Article, Course, Quizz
from .forms import ArticleForm, CourseForm, QuizzForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages

def login(request):
    if request.method == "POST":
        if "registering" in request.POST:
            try:
                email_input = request.POST.get("input-username")
                password_input = request.POST.get("input-password")
                password2_input = request.POST.get("input-repeat-password")
                

                if(not email_input or not password_input or not password2_input):
                    messages.error(request, "Fill all fields")
                    raise Exception("Not all requiered fields are filled")

                if(password_input != password2_input): 
                    messages.error(request, "Passwords dont match")
                    raise Exception("Passwords dont match")
                
                user = Uzytkownik.objects.create_user(email = email_input, password = password_input)
                auth_login(request, user=user)
                    
                return redirect("home")
            except Exception as e:
                messages.info(request, f"Error: {e}")
                print(e)

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
    request.session["title"] = ""

    return render(request, "home.html")


def create_item(request, type):
    if type == "article":
        if request.method == "GET":
            form = ArticleForm()
            
            # Zachowaj dane formularza jeśli są w sesji
            if 'form_data' in request.session:
                form = ArticleForm(request.session['form_data'])
            
            context = { 
                "type" : type,
                "form": form,
            }
            return render(request, "create_item.html", context)

        elif request.method == "POST":
            if "saveAll" in request.POST:
                form = ArticleForm(request.POST)
                
                if form.is_valid():
                    try:
                        article = Article.objects.create(
                            title=form.cleaned_data['title'],
                            lead=form.cleaned_data['lead'],
                            content=form.cleaned_data.get('content', ''),
                            category=form.cleaned_data['category']
                        )
                        # Wyczyść sesję po zapisaniu
                        request.session.pop('form_data', None)
                        
                        messages.success(request, f"Article '{article.title}' created successfully!")
                        return redirect("home")
                    except Exception as e:
                        messages.error(request, f"Error creating article: {e}")
                        print(f"Error message: {e}")
                else:
                    # Jeśli formularz nie jest prawidłowy, zapisz dane w sesji
                    request.session['form_data'] = request.POST.dict()
                    messages.error(request, "Please correct the errors below.")
                
                return redirect("create_item", type=type)
            
    elif type == 'course':
        if request.method == "GET":
            form = CourseForm()
            return render(request, "create_item.html", {"type": type, "form": form})

        if request.method == "POST":
            form = CourseForm(request.POST)
            
            if form.is_valid():
                try:
                    course = form.save()
                    messages.success(request, f"Course '{course.title}' created successfully!")
                    return redirect("home")
                except Exception as e:
                    messages.error(request, f"Error creating course: {e}")
                    print(e)
            else:
                messages.error(request, "Please correct the errors below.")
            
            return render(request, "create_item.html", {"type": type, "form": form})

    else:  # quiz
        if request.method == "GET":
            form = QuizzForm()
            return render(request, "create_item.html", {"type": type, "form": form})

        if request.method == "POST":
            form = QuizzForm(request.POST)
            
            if form.is_valid():
                try:
                    quizz = form.save()
                    messages.success(request, f"Quiz '{quizz.title}' created successfully!")
                    return redirect("home")
                except Exception as e:
                    messages.error(request, f"Error creating quiz: {e}")
                    print(e)
            else:
                messages.error(request, "Please correct the errors below.")
            
            return render(request, "create_item.html", {"type": type, "form": form})


            
def available_articles(request, category):
    articles = Article.objects.filter(category=category)
    return render(request, "articles.html", {"articles": articles})

def available_courses(request, category):
    courses = Course.objects.filter(category=category)
    return render(request, "courses.html", {"courses" : courses})

def available_quizzes(request, category):
    quizz = Quizz.objects.filter(category=category)
    return render(request, "quizzes.html", {"quizzes" : quizz})

def search_item(request):
    pass

def profile(request):
    try:
        if request.user.is_authenticated:
            profile_data = request.user
            print(profile_data)
            return render(request, "profile.html", {"profile_data" : profile_data})
        else: 
            raise Exception("User not authenticated")
    except Exception as e:
        print(e)
        return redirect('profile')