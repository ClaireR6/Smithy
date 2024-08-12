from django import template

register = template.Library()


@register.filter
def custom_range(end, start=1):
    return range(start, end)


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def add(value, arg):
    return value + arg
