from django import template
from main.models import Article, Course, Quizz

register = template.Library()

@register.inclusion_tag("sidebar.html")
def show_categories():
    categories = set()
    articles = list(Article.objects.values_list("category").distinct())
    for category in articles:
        categories.add(category[0])

    courses = list(Course.objects.values_list("category").distinct())
    for category in courses:
        categories.add(category[0])

    quizz = list(Quizz.objects.values_list("category").distinct())
    for category in quizz:
        categories.add(category[0])

    
    return{"categories": list(categories)}

@register.inclusion_tag("navbar.html")
def get_page_name(request):
    subject = str(request).split("/")
    # print(subject)
    if len(subject) > 2:
        result = "".join([(part + "|") for part in subject[1:]])
        ans = result[0:len(result) - 3]
    else:
        ans = subject[1]
    return {"result" : ans.title()}
