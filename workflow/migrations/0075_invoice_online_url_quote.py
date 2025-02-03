# Generated by Django 5.1.4 on 2025-02-03 20:56

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workflow", "0074_bill_xero_last_synced_client_xero_last_synced_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="online_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("xero_id", models.UUIDField(unique=True)),
                ("date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("SENT", "Sent"),
                            ("DECLINED", "Declined"),
                            ("ACCEPTED", "Accepted"),
                            ("INVOICED", "Invoiced"),
                            ("DELETED", "Deleted"),
                        ],
                        default="DRAFT",
                        max_length=50,
                    ),
                ),
                (
                    "total_excl_tax",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "total_incl_tax",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("xero_last_modified", models.DateTimeField(blank=True, null=True)),
                (
                    "xero_last_synced",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("online_url", models.URLField(blank=True, null=True)),
                ("raw_json", models.JSONField(blank=True, null=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workflow.client",
                    ),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quote",
                        to="workflow.job",
                    ),
                ),
            ],
        ),
    ]
