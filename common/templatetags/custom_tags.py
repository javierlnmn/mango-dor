from django import template
from django.utils import timezone
from common.utils import get_app_parameter, get_winners_reveal_date, is_reveal_date_expired

register = template.Library()

@register.simple_tag
def get_app_parameter_tag(key):
    parameter = get_app_parameter(key)
    return parameter(key)

@register.simple_tag
def get_winners_reveal_date_tag():
    return get_winners_reveal_date()

@register.simple_tag
def is_reveal_date_expired_tag():
    return is_reveal_date_expired()