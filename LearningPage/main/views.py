from django.shortcuts import render

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

