from datetime import UTC, datetime
from uuid import uuid4

from django.db import models

META_DEFAULTS = dict(
    checkout_password="SAIPPUAKAUPPIAS",
    checkout_merchant="375917",
)


class PaymentsOrganizationMeta(models.Model):
    organization = models.OneToOneField("core.Organization", on_delete=models.CASCADE, primary_key=True)
    checkout_password = models.CharField(max_length=255)
    checkout_merchant = models.CharField(max_length=255)

    @classmethod
    def get_or_create_dummy(cls, organization=None):
        """
        Creates a POM with Checkout test merchant. Suitable for development, but try to use it in production and you'll get 500 ISE.
        """
        from kompassi.core.models import Organization

        if organization is None:
            organization, uwused = Organization.get_or_create_dummy()

        return cls.objects.get_or_create(
            organization=organization,
            defaults=META_DEFAULTS,
        )

    def get_checkout_params(self, method="POST", t=None):
        if t is None:
            t = datetime.now(UTC)

        return {
            "checkout-account": self.checkout_merchant,
            "checkout-algorithm": "sha256",
            "checkout-method": method,
            "checkout-nonce": str(uuid4()),
            "checkout-timestamp": t.isoformat(),
        }
