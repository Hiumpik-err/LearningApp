from django import template
from main.models import Article, Course, Quizz

register = template.Library()

@register.inclusion_tag("components/articles.html")
def get_latest_articles():
    aricles = list(Article.objects.all().order_by("-upload_data")[:3])

    return {"articles": aricles}

@register.inclusion_tag("components/tasks.html")
def get_latest_courses():
    tasks = list(Course.objects.all().order_by("-upload_data")[:3])

    return {"tasks": tasks}

@register.inclusion_tag("components/quizzes.html")
def get_latest_quizzes():
    quizzes = list(Quizz.objects.all().order_by("-upload_data")[:3])

    return {"quizzes": quizzes}

@register.inclusion_tag("components/navbar.html", takes_context=True)
def get_current_path(context):
    request = context.get("request")
    if request:
        path = request.path
        path = path.strip("/")
        path_split = str(path).split("/")
        
        match(path_split):
            case ["content_view", *res]:
                res = "".join(res)
                path = f"content/{res}"
    

    return {"path" : str(path).title(), "current_user" : request.user}

