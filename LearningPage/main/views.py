from django.shortcuts import render
from . import function as fn
from .forms import WpisForm


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
        pass
    elif type == 'task':
        pass
    else:
        form = WpisForm

    return render(request, "create_item.html", {"form": form})


def search_item(request):
    pass