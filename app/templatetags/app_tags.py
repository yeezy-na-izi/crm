from django import template
from django.urls import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, url):
    cur_url = resolve(context['request'].path).url_name
    if cur_url.startswith(url):
        return 'active'
    return ''
