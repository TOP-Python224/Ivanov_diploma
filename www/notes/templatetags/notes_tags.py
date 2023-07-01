from django import template
from models.models import *
from django.db.models import Q
from django.core.paginator import Paginator

register = template.Library()

@register.simple_tag()
def note_catigories():
    return Category.objects.all()

@register.simple_tag(takes_context=True)
def filter_cat(context):
    request = context['request']
    search_list = request.GET.get('s', '')
    filter = context['cats']
    if search_list:
        contact_list = Articles.objects.filter(Q(title__icontains=search_list) | Q(text__icontains=search_list), is_published=True)
    elif filter:
        contact_list = Articles.objects.filter(cat__slug=filter, is_published=True)
    else:
        contact_list = Articles.objects.filter(is_published=True)
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page', 1)
    context['pg'] = int(page_number)
    page_obj = paginator.get_page(page_number)
    return page_obj

