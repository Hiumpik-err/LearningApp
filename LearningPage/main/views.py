from django.shortcuts import render, redirect
from .models import Uzytkownik, Article, Course, Quizz
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages

def login(request):
    if request.method == "POST":
        if "registering" in request.POST:

            email_input = request.POST.get("input-username")
            password_input = request.POST.get("input-password")
            password2_input = request.POST.get("input-repeat-password")
            

            if(not email_input or not password_input or not password2_input):
                messages.error(request, "Fill all fields")
                raise Exception("Not all requiered fields are filled")

            if(password_input != password2_input): 
                messages.error(request, "Passwords dont match")
                raise Exception("Passwords dont match")
            try:
                user = Uzytkownik.objects.create_user(email = email_input, password = password_input)
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
    request.session["current_count"] = 1
    #request.session["images"] = []
    request.session["header_list"] = ""
    request.session["content_list"] = ""
    request.session["title"] = ""

    return render(request, "home.html")

def item_view(request):
    return render(request, "item_view.html")


def create_item(request, type):
    if type == "article":
        if request.method == "GET":
            current_count = request.session.get("current_count", "")
            header_list = request.session.get("header_list", "")
            content_list = request.session.get("content_list", "")
            title = request.session.get("title", "")
            category = request.session.get("category", "")
            context = { "type" : type,
                        "current_count" : current_count,
                        "header_count" : reversed(list(range(current_count))),
                        "header_list" : header_list,
                        "content_list" : content_list,
                        "title" : title,
                        "category" : category
                    }
            return render(request, "create_item.html", context)

        elif request.method == "POST":
            if "add_new_section" in request.POST:
                request.session["title"] = request.POST.get("title", "") #NOTE doesnt work with space, later check why
                request.session["category"] = request.POST.get("category", "")

                header_list = []
                content_list = []

                for i in range(request.session.get("current_count")):
                    header_list.append(request.POST.get("header_" + str(i)).strip())
                    content_list.append(request.POST.get("content_" + str(i)).strip())

                request.session["header_list"] = list(header_list)
                request.session["content_list"] = list(content_list)


                request.session["current_count"] = int(request.session.get("current_count")) + 1

                return redirect("create_item", type=type)
            
            if "saveAll" in request.POST:
                headers = []
                contents = []
                title = request.POST.get("title", "")
                category = request.POST.get("category", "")
                current_count = int(request.session.get("current_count"))

                for index in range(current_count):
                    header = request.POST.get("header_" + str(index)).strip()
                    content = request.POST.get("content_" + str(index)).strip()
                    headers.append(header)
                    contents.append(content)

                try:
                    article = Article.objects.create(
                        title = title,
                        wholeContent = {
                            "headers": list(headers),
                            "contents": list(contents)
                        },
                        category = category
                    )
                    return redirect("home")
                except Exception as e:
                    print(f"Error message: {e}")
                

            if not "add_new_section" in request.POST and not "saveAll" in request.POST:
                
                for key in request.POST:
                    if(key.startswith("delete_section_")):
                        remove_index = int(key.split("_")[-1])

                        headers = []
                        contents = []
                        current_count = int(request.session.get("current_count"))

                        for index in range(current_count):
                            if index != remove_index:
                                header = request.POST.get("header_" + str(index)).strip()
                                content = request.POST.get("content_" + str(index)).strip()
                                headers.insert(0,header)
                                contents.insert(0,content)

                        request.session["header_list"] = headers
                        request.session["content_list"] = contents
                        request.session["current_count"] = int(request.session.get("current_count")) - 1

                        return redirect("create_item", type)
    elif type == 'course':
        if request.method == "GET":
            return render(request, "create_item.html", {"type": type})

        if request.method == "POST":
            category = request.POST.get("category", "")
            title = request.POST.get("title", "")
            question = request.POST.get("question", "")
            answers = request.POST.get("answers", "")

            try:
                course = Course.objects.create(
                    category=category, 
                    title=title,
                    question=question,
                    answers=answers
                )
                print("Objekt został stworzony")
                return redirect("home")
            except Exception as e:
                print(e)
                return redirect("create_item", type=type)

    else:
        if request.method == "GET":
            return render(request, "create_item.html", {"type": type})

        if request.method == "POST":
            category = request.POST.get("category", "")
            title = request.POST.get("title", "")
            description = request.POST.get("description", "")
            link = request.POST.get("link", "")

            try:
                quizz = Quizz.objects.create(
                    category=category, 
                    title=title,
                    description=description,
                    link=link
                )
                print("Objekt został stworzony")
                return redirect("home")
            except Exception as e:
                print(e)
                return redirect("create_item", type=type)


            
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