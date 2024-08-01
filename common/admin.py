from django.contrib import admin
from .models import Parameter

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
