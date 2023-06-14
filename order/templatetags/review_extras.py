from django import template

register = template.Library()

# @register.simple_tag 

@register.filter(name='times')
def times(number):
    return range(round(number))


