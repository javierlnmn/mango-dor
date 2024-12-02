from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from common.models import SiteParameters

from .models import Category, Vote
from .utils import get_current_category_for_user
from candidates.models import Candidate

class CategoryListView(ListView):
    model = Category
    paginate_by = 6
    ordering = 'name'


class CategoryDetailView(DetailView):
    model = Category


class VotingView(LoginRequiredMixin, View):
    
    def dispatch(self, *args, **kwargs):
        
        is_winners_reveal_date_passed = SiteParameters.objects.get(id=1).is_winners_reveal_date_passed
            
        if is_winners_reveal_date_passed:
            return redirect('voting:voting-results')
        
        return super(VotingView, self).dispatch(*args, **kwargs)
    
    def get_categories(self):
        cached_categories = cache.get('categories_cache')

        if not cached_categories:
            cached_categories = Category.objects.all().order_by('name')
            cache.set('categories_cache', cached_categories, timeout=3600)  # Cache for 1 hour

        return cached_categories
    
    def validate_voting(self, voting_options_count, candidates_count, voting_points_count, candidate_vote_count):
        # If there are repeated candidates
        if voting_points_count != candidate_vote_count:
            return False
        
        # If there are more candidates than available votes, and the recieved votes
        # aren't the same as all available votes
        if candidates_count > voting_options_count and voting_points_count != voting_options_count:
            return False
        
        # If there are more or the same available votes than candidates, and the recieved votes
        # aren't the number of candidates
        if voting_options_count >= candidates_count and voting_points_count != candidates_count:
            return False
        
        return True
        
    
    def get(self, request):
        current_category, current_category_number, total_categories_number = get_current_category_for_user(request.user)
        
        if not current_category:
            return redirect('voting:voting-completion')

        candidates = Candidate.objects.all()
        
        voting_points = [value for value, _ in Vote.VOTING_POINTS_CHOICES]
        
        context = {
            'current_category': current_category,
            'current_category_number': current_category_number,
            'total_categories_number': total_categories_number,
            'candidates': candidates,
            'voting_points': voting_points
        }
        
        return render(request, 'voting/voting.html', context)
    
    def post(self, request):
        current_category, _, _ = get_current_category_for_user(request.user)
        if not current_category:
            return redirect('voting:voting-completion')

        voting_points_list = [value for value, _ in Vote.VOTING_POINTS_CHOICES]
        voting_points_choices = {}
        for points in voting_points_list:
            try:
                candidate_id = int(request.POST.get(f'voting_choice_{points}_points', None))
                
                # If candidate doesn't exists
                if not Candidate.objects.filter(id=candidate_id).exists():
                    return redirect('voting:voting')
                
                voting_points_choices[points] = candidate_id
            except (ValueError, TypeError):
                return redirect('voting:voting')
        
        candidates_count = Candidate.objects.all().count()
        voting_points_count = len(set(voting_points_choices.keys()))
        candidate_vote_count = len(set(voting_points_choices.values()))
        
        is_valid_voting = self.validate_voting(len(voting_points_list), candidates_count, voting_points_count, candidate_vote_count)
        
        if not is_valid_voting:
            return redirect('voting:voting')
        
        for vote_points, vote_candidate in voting_points_choices.items():
            Vote.objects.create(
                user=request.user,
                candidate_id=vote_candidate,
                category=current_category,
                points=vote_points
            )
            
        return redirect('voting:voting')


class VotingCompletionView(LoginRequiredMixin, TemplateView):
    template_name = 'voting/voting_completion.html'

    def dispatch(self, request, *args, **kwargs):
        
        is_winners_reveal_date_passed = SiteParameters.objects.get(id=1).is_winners_reveal_date_passed
            
        if is_winners_reveal_date_passed:
            return redirect('voting:voting-results')
        
        current_category, _, _ = get_current_category_for_user(request.user)
        if current_category:
            return redirect('voting:voting')
        
        return super(VotingCompletionView, self).dispatch(request, *args, **kwargs)


class VotingResultsView(LoginRequiredMixin, TemplateView):
    template_name = 'voting/voting_results.html'
    
    def dispatch(self, *args, **kwargs):
        
        is_winners_reveal_date_passed = SiteParameters.objects.get(id=1).is_winners_reveal_date_passed
            
        if not is_winners_reveal_date_passed:
            return redirect('voting:voting')
        
        return super(VotingResultsView, self).dispatch(*args, **kwargs)
