from django.shortcuts import render
from . import function as fn


def home(request):

    return render(request, "home.html")

def item_view(request):

    return render(request, "item_view.html")

def create_item(request, type):
    context = {"type" : type}
    return render(request, "create_item.html", context)


def search_item(request):
    pass