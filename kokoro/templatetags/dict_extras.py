from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    """
    Template filter to look up a value in a dict by key.
    Usage: {{ mydict|dict_get:some_key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
