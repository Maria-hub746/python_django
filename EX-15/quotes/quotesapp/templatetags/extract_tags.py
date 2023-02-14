from django import template

register = template.Library()

def tags(quotes_tags):
    return quotes_tags.all()

register.filter('tags', tags)
