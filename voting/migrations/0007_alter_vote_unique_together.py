# Generated by Django 5.0.6 on 2024-10-15 09:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0006_alter_candidate_slug'),
        ('voting', '0006_alter_vote_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('user', 'candidate', 'category')},
        ),
    ]
