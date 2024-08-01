from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from .models import Parameter

def get_app_parameter(key):
    try:
        return Parameter.objects.get(key=key).value
    except ObjectDoesNotExist:
        return None

def get_winners_reveal_date():
    winners_reveal_date_string = get_app_parameter('WINNERES_REVEAL_DATE')
    try:
        return date.fromisoformat(winners_reveal_date_string)
    except (ObjectDoesNotExist, ValueError):
        return None
    
def is_reveal_date_expired():
    today = date.today()
    reveal_date = get_winners_reveal_date()
    return False if reveal_date > today else True