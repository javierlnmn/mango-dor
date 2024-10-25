from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Category

class CategoryListView(ListView):
    model = Category
    paginate_by = 6
    ordering = 'name'

class CategoryDetailView(DetailView):
    model = Category