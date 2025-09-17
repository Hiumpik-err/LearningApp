from django.shortcuts import render, redirect
from . import function as fn
from .forms import ArticleForm, TaskForm



def home(request):
    context = {
        'card' : {  "id" : 1,
                    "title": "Quadratic Formula",
                    "description": "It's fine",
                    "content" : "Delta"
                 }
    }
    return render(request, "index.html", context)

def item_view(request, item_id):

    context = {
        'card' : {  "title": "Quadratic Formula",
                    "description": "It's fine",
                    "content" : "Delta"
                 }
    }
    return render(request, "item_view.html", context)

def create_item(request, type):
    if request.method == "GET":
        if type == "article":
            form = ArticleForm()
        elif type == 'task':
            form = TaskForm()
        else:
            pass
    elif request.method == "POST":
        if type == "article":
            if fn.create_article(request.POST):
                return redirect("home")
        elif type == "task":
            if fn.create_task(request.POST):
                return redirect("home")
        else:
            if fn.create_quizz(request.POST):
                return redirect("home")

    return render(request, "create_item.html", {"form" : form, "type" : type})


def search_item(request):
    pass