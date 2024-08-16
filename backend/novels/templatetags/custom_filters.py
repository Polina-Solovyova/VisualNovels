from django import template

register = template.Library()

@register.filter
def dict_item(dictionary, key):
    """Returns the value for the given key in the dictionary."""
    return dictionary.get(key)
