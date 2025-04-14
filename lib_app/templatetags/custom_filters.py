from django import template

register = template.Library()

@register.filter
def stars(value):
    """指定された数値分の★を返す"""
    try:
        value = int(value)
        return "★" * value
    except (ValueError, TypeError):
        return ""