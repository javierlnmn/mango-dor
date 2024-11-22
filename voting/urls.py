from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('categories/<str:slug>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('', views.VotingView.as_view(), name='voting'),
    path('completed/', views.VotingCompletionView.as_view(), name='voting-completion'),
]
