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
    
    def get(self, request):
        categories = Category.objects.all().order_by('name')
        
        current_category_number = 0
        total_categories_number = Category.obejcts.all().count()
        
        for index, category in enumerate(categories):
            user_votes_completed = category.user_category_voting_complete(request.user)
            
            if not user_votes_completed:
                current_category = category
                current_category_number = index + 1
                break
        
        if not current_category:
            return redirect('voting:voting-completion')

        # We check if a candidate has been already voted by the user inside the template
        candidates = Candidate.objects.all()
        
        context = {
            'current_category': current_category,
            'current_category_number': current_category_number,
            'total_categories_number': total_categories_number,
            'candidates': candidates,
        }
        return render(request, 'voting/voting.html', context)
    
    # def post(self, request,):
    #     return


class VotingCompletionView(LoginRequiredMixin, TemplateView):
    template_name = 'voting/voting_completion.html'