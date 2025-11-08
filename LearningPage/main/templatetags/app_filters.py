from django import template

register = template.Library()

@register.filter(name='get') 
def get_item(list, key):
    try:
        print(f"{list} { key}")
        return list[key]
    except:
        return ""