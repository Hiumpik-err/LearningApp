from django.shortcuts import render
from . import function as fn


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