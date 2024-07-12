from django.contrib import admin
from .models import Nationality, Gender, Candidate, CandidateImage

@admin.register(CandidateImage)
class CandidateImageAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'image_preview')

    def image_preview(self, obj):
        return obj.image.url if obj.image else None

    image_preview.short_description = 'Image Preview'

@admin.register(Nationality)
class NationalityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age', 'linkedin_profile')
    search_fields = ('name', 'surname', 'nationality__name', 'gender__name')
    list_filter = ('gender', 'nationality')
    filter_horizontal = ('nationality',)

    fieldsets = (
        ('Candidate', {
            'fields': ('name', 'surname', 'age', 'gender', 'nationality',)
        }),
        ('Additional Information', {
            'fields': ('description', 'education', 'experience', 'skills', 'languages', 'linkedin_profile'),
        }),
    )

    class CandidateImageInline(admin.TabularInline):
        model = CandidateImage
        extra = 1

    inlines = [CandidateImageInline]
