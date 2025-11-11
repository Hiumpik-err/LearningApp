from django import template
from main.models import Article

register = template.Library()

@register.inclusion_tag("sidebar.html")
def show_categories():
    articles = list(Article.objects.values_list("category").distinct())
    categories = [category[0] for category in articles]
    
    return{"categories": categories}