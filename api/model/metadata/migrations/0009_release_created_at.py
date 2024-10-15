# Generated by Django 5.0.2 on 2024-10-11 12:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metadata", "0008_release"),
    ]

    operations = [
        migrations.AddField(
            model_name="release",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
