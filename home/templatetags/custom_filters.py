from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """Splits the string by the given separator (arg) and returns the item at the specified index."""
    if value:
        return value.split(arg)[1] if len(value.split(arg)) > 1 else ""
    return ""
