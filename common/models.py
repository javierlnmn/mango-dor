from django.db import models

# Create your models here.
class Parameter(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f'{self.key}: {self.description}'