from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Vote, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'slug', 'image')
    search_fields = ('name', 'code')
    list_filter = ('name', 'code')
    
    prepopulated_fields = {"slug": ("name",)}

class VoteInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        votes = {}
        
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                user = form.cleaned_data.get('user')
                category = form.cleaned_data.get('category')
                points = form.cleaned_data.get('points')
                candidate = form.cleaned_data.get('candidate')

                if (user, category) not in votes:
                    votes[(user, category)] = {"points": set(), "candidates": set()}

                if points in votes[(user, category)]["points"]:
                    raise ValidationError(f'The user {user} has already assigned {points} points in this category.')

                if candidate in votes[(user, category)]["candidates"]:
                    raise ValidationError(f'The user {user} has already voted for {candidate} in this category.')

                votes[(user, category)]["points"].add(points)
                votes[(user, category)]["candidates"].add(candidate)

        for (user, category), data in votes.items():
            if len(data["points"]) > 3:
                raise ValidationError(f'The user {user} cannot vote more than 3 times in the category {category}.')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate', 'category', 'points')
    list_filter = ('category', 'user', 'candidate')
    search_fields = ('user__username', 'candidate__name', 'category__name')
    ordering = ('user', 'category', 'points')
    
    def save_model(self, request, obj, form, change):
        obj.clean()
        super().save_model(request, obj, form, change)
