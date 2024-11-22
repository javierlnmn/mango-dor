# Generated by Django 5.0.6 on 2024-10-15 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='voting.category'),
            preserve_default=False,
        ),
    ]