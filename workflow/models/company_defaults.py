from django.core.exceptions import ValidationError
from django.db import models, transaction


class CompanyDefaults(models.Model):
    company_name = models.CharField(max_length=255, primary_key=True)
    is_primary = models.BooleanField(default=True, unique=True)
    time_markup = models.DecimalField(max_digits=5, decimal_places=2, default=0.3)
    materials_markup = models.DecimalField(max_digits=5, decimal_places=2, default=0.2)
    charge_out_rate = models.DecimalField(
        max_digits=6, decimal_places=2, default=105.00
    )  # rate per hour
    wage_rate = models.DecimalField(
        max_digits=6, decimal_places=2, default=32.00
    )  # rate per hour

    starting_job_number = models.IntegerField(default=1, help_text="Helper field to set the starting job number based on the latest paper job")

    # Default working hours (Mon-Fri, 7am - 3pm)
    mon_start = models.TimeField(default="07:00")
    mon_end = models.TimeField(default="15:00")
    tue_start = models.TimeField(default="07:00")
    tue_end = models.TimeField(default="15:00")
    wed_start = models.TimeField(default="07:00")
    wed_end = models.TimeField(default="15:00")
    thu_start = models.TimeField(default="07:00")
    thu_end = models.TimeField(default="15:00")
    fri_start = models.TimeField(default="07:00")
    fri_end = models.TimeField(default="15:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_xero_sync = models.DateTimeField(null=True, blank=True, help_text="The last time Xero data was synchronized")
    last_xero_deep_sync = models.DateTimeField(null=True, blank=True, help_text="The last time a deep Xero sync was performed (looking back 90 days)")

    class Meta:
        verbose_name = "Company Defaults"
        verbose_name_plural = "Company Defaults"

    def save(self, *args, **kwargs):
        if not self.pk and CompanyDefaults.objects.exists():
            raise ValidationError("There can be only one CompanyDefaults instance")
        self.is_primary = True
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance.
        This is the preferred way to get the CompanyDefaults instance.
        """
        with transaction.atomic():
            return cls.objects.get()

    def __str__(self):
        return self.company_name
