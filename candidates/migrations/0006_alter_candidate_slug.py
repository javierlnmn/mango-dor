# Generated by Django 5.0.6 on 2024-07-31 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0005_candidate_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
