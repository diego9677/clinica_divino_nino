from django import template

register = template.Library()


@register.filter(name='add_clss')
def add_clss(field, clss):
    return field.as_widget(attrs={'class': clss})
