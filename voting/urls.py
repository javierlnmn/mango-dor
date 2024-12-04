from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('', views.VotingView.as_view(), name='voting'),
    path('completion/', views.VotingCompletionView.as_view(), name='voting-completion'),
    path('results/', views.VotingResultsView.as_view(), name='voting-results'),
    path('results/<str:slug>/', views.VotingResultsView.as_view(), name='voting-results'),
]
