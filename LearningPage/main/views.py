from django.shortcuts import render
from . import function as fn


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
    if type == "article":
        fn.create_article(request.POST)
    elif type == 'task':
        fn.create_task(request.POST)
    else:
        fn.create_quizz(request.POST)

    return render(request, "create_item.html")


def search_item(request):
    pass