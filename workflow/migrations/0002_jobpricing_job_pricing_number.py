# Generated by Django 5.0.6 on 2024-09-23 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workflow", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobpricing",
            name="job_pricing_number",
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
