from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from datetime import date

from common.models import SiteParameters


def get_winners_reveal_date():
    site_settings = SiteParameters.objects.get(id=1)
    winners_reveal_date_string = site_settings.winners_reveal_date
    try:
        return date.fromisoformat(winners_reveal_date_string)
    except (ObjectDoesNotExist, ValueError):
        return None


def is_reveal_date_expired():
    reveal_date = get_winners_reveal_date()
    today = timezone.now()
    return False if reveal_date > today else True