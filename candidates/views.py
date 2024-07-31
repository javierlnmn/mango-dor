from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Candidate


class CandidateListView(ListView):
    model = Candidate
    paginate_by = 6

class CandidateDetailView(DetailView):
    model = Candidate