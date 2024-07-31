from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Candidate


class CandidateListView(ListView):
    model = Candidate
    paginate_by = 6


