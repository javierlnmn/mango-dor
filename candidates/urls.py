from django.urls import path
from . import views

app_name = 'candidates'

urlpatterns = [
    path('', views.CandidateListView.as_view(), name='candidates-list'),
    path('<str:slug>/', views.CandidateDetailView.as_view(), name='candidate-detail'),
]
