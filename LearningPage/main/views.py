from password_validation.policy import PasswordPolicy
from django.shortcuts import render, redirect
from .models import Uzytkownik, Article, Course, Quizz
from .forms import ArticleForm, CourseForm, QuizzForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from django.db.models import Q

def login(request):
    if request.method == "POST":
        if "register" in request.POST:
            try:
                fullname = request.POST.get("fullname", "")
                email = request.POST.get("email", "")
                password = request.POST.get("password", "")
                repeat_password = request.POST.get("repeat_password", "")

                password_policy = PasswordPolicy(
                        min_length=10,
                        uppercase=2,
                        lowercase=2,
                        numbers=2,
                        symbols=1,
                        max_length=50
                )


                if not all([fullname, email, password, repeat_password]):
                    raise Exception("Fill all empty spaces")
                
                if " " not in fullname:
                    raise Exception("Invalid fullname (space requiered)")
                
                if not password_policy.validate(password):
                    raise Exception("Invalid Password, stronger required")

                if str(password).strip() != str(repeat_password).strip():
                    raise Exception("Invalid passwords, passwords dont match")

                user = Uzytkownik.objects.create_user(email = email, password=password )
                print(user)
                auth_login(request, user=user)
                    
                return redirect("home")
            except Exception as e:
                messages.info(request, f"Error: {e}")
                print(e)
                return redirect("login")
                

        if "login" in request.POST:
            try:
                password_input = request.POST.get("password", "")
                email = request.POST.get("email", "")

                user = authenticate(request, email=email, password=password_input)

                if not user:
                    #   messages.error(request, "User not found. womp womp ")
                    raise Exception("User not found")
                
                auth_login(request, user)
                return redirect("home")

            except Exception as e:
                    messages.error(request, f"Error: {e}")
                    return redirect("login")
                

    return render(request, "login.html")

def home(request):
    if request.method == "GET":
        request.session["title"] = ""
        return render(request, "home.html", {"request" : request.path})
    
    return render(request, "home.html")
        

def create_item(request, type):
    if type == "article":
        if request.method == "POST" and "showElement" in request.POST:
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
        if request.method == "POST" and "showElement" in request.POST:
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
        if request.method == "POST" and "showElement" in request.POST:
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



def content_view(request, type):

    article_categories = Article.objects.values_list('category', flat=True).distinct()
    course_categories = Course.objects.values_list('category', flat=True).distinct()
    quizz_categories = Quizz.objects.values_list('category', flat=True).distinct()
    
    categories = sorted(set(list(article_categories) + list(course_categories) + list(quizz_categories)))

    context = {"categories": categories}
    
    if request.method == "GET":
        if type == 'articles':
            articles = Article.objects.all().order_by('-upload_data')
            context["articles"] = articles
        elif type == 'courses':
            courses = Course.objects.all().order_by('-upload_data')
            context["courses"] = courses
        elif type == 'quizzes':
            quizzes = Quizz.objects.all().order_by('-upload_data')
            context["quizzes"] = quizzes

    elif request.method == "POST":
        category = request.POST.get("category", "")

        if type == 'articles':
            articles = Article.objects.all().order_by('-upload_data')
            articles = articles.filter(category__iexact=category) if category != "" else articles
            context["articles"] = articles
        elif type == 'courses':
            courses = Course.objects.all().order_by('-upload_data')
            courses = courses.filter(category__iexact=category) if category != "" else courses
            context["courses"] = courses
        elif type == 'quizzes':
            quizzes = Quizz.objects.all().order_by('-upload_data')
            quizzes = quizzes.filter(category__iexact=category) if category != "" else quizzes
            context["quizzes"] = quizzes
      
    
    return render(request, 'content_view.html', context)


def profile(request):
    print("delete_account" in request.POST)
    if request.method == "GET":
        try:
            if request.user.is_authenticated:
                profile_data = request.user
                return render(request, "profile.html", {"profile_data" : profile_data})
            else: 
                raise Exception("User not authenticated")
        except Exception as e:
            print(e)
            return redirect('profile')
        
    if request.method == "POST" and "logout" in request.POST:
        logout(request)
        return redirect("/")
    elif request.method == "POST" and "admin_request" in request.POST:
        pass
    elif request.method == "POST" and "delete_account" in request.POST:
        print("jestem w usuwaniu")
        try:
            user = request.user
            logout(request)
            user.delete()
            return redirect("/")
            
        except Exception as e:
            print(e)
            return redirect("login")
    
def item_view(request, type, id):
    answer = request.session.get("result", "")
    if request.method == "GET":
        if type == "articles":
            article = Article.objects.get(ArticleId=id)
            return render(request, "item_view.html", {"article": article, "type":type, "result": False, "answer":answer})
        elif type == "courses":
            course = Course.objects.get(CourseId=id)
            return render(request, "item_view.html", {"course": course, "type": type, "result": False, "answer":answer})
        elif type == "quizzes":
            quizz = Quizz.objects.get(QuizzId = id)
            return render(request, "item_view.html", {"quizz": quizz, "type": type, "result": False, "answer":answer})
        elif type == "result":
            course = Course.objects.get(CourseId=id)
            return render(request, "item_view.html", {"course": course, "type": "courses", "result": True, "answer":answer})

        
    elif request.method == "POST":
        answer = str(request.POST.get("answer", "")).strip().lower()
        course_answer = Course.objects.get(CourseId=id).answers.strip().lower()

        if answer != course_answer:
            request.session["result"] = "❌"
        
        else:
            request.session["result"] = "✅"
        
        return redirect("item_view", type="result", id=id)

def update(request, type, id):
    try:
        if type == "articles":
            article = Article.objects.get(ArticleId=id)
            print("jest w artykule")
            if request.method == "GET":
                form = ArticleForm(instance=article)
                return render(request, "edit_view.html", {"type": type, "form": form})
            
            elif request.method == "POST":
                form = ArticleForm(request.POST, instance= article)
                form.save()

                return redirect("item_view", type = type, id=article.ArticleId)
            
        elif type == "courses":
            course = Course.objects.get(CourseId=id)
            if request.method == "GET":
                form = CourseForm(instance=course)
                return render(request, "edit_view.html", {"type": type, "form": form})
            
            elif request.method == "POST":
                form = CourseForm(request.POST, instance= course)

                form.save()
                return redirect("item_view", type =type, id=course.CourseId)
            
        elif type == 'quizzes':
            quizz = Quizz.objects.get(QuizzId = id)
            if request.method == "GET":
                form = QuizzForm(instance=quizz)
                return render(request, "edit_view.html", {"type": type, "form": form})
            
            elif request.method == "POST":
                form = QuizzForm(request.POST, instance=quizz)
                form.save()
                return redirect("home")
    except Exception as e:
        print(e)
        return redirect("update", type=type, id=id)

        
def search(request):
    if "allContent" in request.POST:
        searched_value = request.POST.get("searched_value")
        articles = list(Article.objects.filter(Q(title__icontains=searched_value) | 
                                          Q(content__icontains=searched_value)
                                        ))
        courses = list(Course.objects.filter(title__icontains=searched_value))
        quizzes = list(Quizz.objects.filter(Q(title__icontains=searched_value) | 
                                       Q(description__icontains=searched_value)))
        
        context = {
            "articles": articles,
            "courses": courses,
            "quizzes" : quizzes,
            "search_filter": searched_value
        }


    return render(request, "search_items_view.html", context)

