import logging
import uuid

from django.db import models

logger = logging.getLogger(__name__)

class Client(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # Internal UUID
    xero_contact_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    # Optional because not all prospects are synced to Xero
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_account_customer = models.BooleanField(
        default=False
    )  # Account vs cash customer flag
    xero_last_modified = models.DateTimeField(null=False, blank=False)

    raw_json = models.JSONField(
        null=True, blank=True
    )  # For debugging, stores the raw JSON from Xero
    django_created_at = models.DateTimeField(auto_now_add=True)
    django_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def validate_for_xero(self):
        """
        Validate if the client data is sufficient to sync to Xero.
        """
        if not self.name:
            logger.error(f"Client {self.id} does not have a valid name.")
            return False
        if not self.email and not self.phone:
            logger.error(
                f"Client {self.id} needs either a valid email or phone number."
            )
            return False
        # Add more checks as necessary for other fields
        return True

    def get_client_for_xero(self):
        """
        Return the client data in a format suitable for syncing to Xero.
        Handles None values explicitly to ensure proper serialization.
        """
        # Logging all data for debugging
        logger.debug(f"Preparing client for Xero sync: ID={self.id}, Name={self.name}")

        # Ensure required fields are present
        if not self.name:
            raise ValueError(
                f"Client {self.id} is missing a name, which is required for Xero.")

        # Prepare serialized data
        client_dict = {
            "contact_id": self.xero_contact_id or "",  # Empty string if None
            "name": self.name,  # Required by Xero, must not be None
            "email_address": self.email or "",  # Empty string if None
            "phones": [
                {
                    "phone_type": "DEFAULT",
                    "phone_number": self.phone or "",  # Empty string if None
                }
            ],
            "addresses": [
                {
                    "address_type": "STREET",
                    "attention_to": self.name,
                    "address_line1": self.address or "",  # Empty string if None
                }
            ],
            "is_customer": self.is_account_customer,  # Boolean, always valid
        }

        # Log the final serialized data
        logger.debug(f"Serialized client data for Xero: {client_dict}")
        return client_dict


class Supplier(Client):
    """
    A Supplier is simply a Client with additional semantics.
    """
    class Meta:
        proxy = True
