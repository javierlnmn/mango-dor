from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from candidates.models import Candidate


class Category(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    winner = models.ForeignKey(Candidate, on_delete=models.PROTECT, related_name="won_categories", blank=True, null=True)
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def user_category_voting_complete(self, user):
        votes_in_category = self.votes.filter(user=user).count()
        return False if votes_in_category < 3 else True

    def __str__(self):
        return f'{self.name} ({self.code})'


class Vote(models.Model):

    VOTING_POINTS_CHOICES = [
        (1, '1 Points'),
        (2, '2 Points'),
        (4, '4 Points'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='votes')
    points = models.IntegerField(choices=VOTING_POINTS_CHOICES)
    
    class Meta:
        unique_together = ["user", "candidate", "category"]
        
    def clean(self):
        existing_vote = Vote.objects.filter(user=self.user, candidate=self.candidate, category=self.category)
        if existing_vote.exists():
            raise ValidationError('You have already voted for this candidate in this category.')

        duplicate_points = Vote.objects.filter(user=self.user, category=self.category, points=self.points)
        if duplicate_points.exists():
            raise ValidationError(f'You have already assigned {self.get_points_display()} points in this category.')

        votes_in_category = Vote.objects.filter(user=self.user, category=self.category).count()
        if votes_in_category >= 3:
            raise ValidationError('You have already voted 3 times in this category.')

    def __str__(self):
        return f"{self.user} voted {self.get_points_display()} points for {self.candidate} in {self.category}"