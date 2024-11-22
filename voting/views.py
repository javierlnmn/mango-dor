from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Vote
from candidates.models import Candidate


class CategoryListView(ListView):
    model = Category
    paginate_by = 6
    ordering = 'name'


class CategoryDetailView(DetailView):
    model = Category


class VotingView(LoginRequiredMixin, View):
    
    def get_categories(self):
        cached_categories = cache.get('categories_cache')

        if not cached_categories:
            cached_categories = Category.objects.all().order_by('name')
            cache.set('categories_cache', cached_categories, timeout=3600)  # Cache for 1 hour

        return cached_categories
    
    def get_current_category_for_user(self, user):
        categories = self.get_categories()
        total_categories_number = categories.count()
        current_category = None
        current_category_number = 0
        
        for index, category in enumerate(categories):
            user_votes_completed = category.user_category_voting_complete(user)
            
            if not user_votes_completed:
                current_category = category
                current_category_number = index + 1
                break
        
        return current_category, current_category_number, total_categories_number
    
    def get(self, request):
        current_category, current_category_number, total_categories_number = self.get_current_category_for_user(request.user)
        
        if not current_category:
            return redirect('voting:voting-completion')

        candidates = Candidate.objects.all()
        
        context = {
            'current_category': current_category,
            'current_category_number': current_category_number,
            'total_categories_number': total_categories_number,
            'candidates': candidates,
        }
        
        return render(request, 'voting/voting.html', context)
    
    def post(self, request):
        current_category, _, _ = self.get_current_category_for_user(request.user)
        
        if not current_category:
            return redirect('voting:voting-completion')
        
        voting_points_list = [1, 2, 4]
        voting_points_choices = {}
        
        for points in voting_points_list:
            voting_points_choices[points] = request.POST.get(f'voting_choice_{points}_points', None)
        
        # In case an input name was modified
        if len(voting_points_choices) is not len(voting_points_list):
            return redirect('voting:voting')
        
        # In case a vote value was None
        for voting_value in voting_points_choices.values():
            if not voting_value:
                return redirect('voting:voting')
        
        # In case they repeated candidate
        if len(set(voting_points_choices.values())) != len(voting_points_list):
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