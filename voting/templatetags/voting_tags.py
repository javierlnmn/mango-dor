from django import template

from voting.models import Vote

register = template.Library()

@register.filter
def candidate_user_category_vote_exists(candidate, user, category):
        is_voted = candidate.votes.filter(user=user, category=category).exists()
        return True if is_voted else False