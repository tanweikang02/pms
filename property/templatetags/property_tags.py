from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def format_booking_name(file_name):
    if file_name.startswith('booking/'):
        return file_name[8:]


@register.filter
@stringfilter
def format_sale_name(file_name):
    if file_name.startswith('sale/'):
        return file_name[5:]
