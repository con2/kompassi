from django.core.validators import RegexValidator
from django.db import models

from kompassi.labour.models import SignupExtraBase

validate_email_alias = RegexValidator(
    regex=r"^[a-z0-9.-]+$",
    message="Only lowercase letters a-z, digits 0-9, the dot and the hyphen are allowed.",
)


class SignupExtra(SignupExtraBase):
    email_alias = models.CharField(
        blank=True,
        default="",
        max_length=32,
        verbose_name="Email alias",
        help_text=(
            "By default everyone will get a firstname.lastname@ropecon.fi Google Account with a "
            "firstname.lastname@solmukohta.eu alias. If you're happy with that, leave this empty. "
            "However, if you want the part before @ to be something else than the first and last "
            "name in your Kompassi profile, enter it and only it here, nothing else. "
            "Allowed characters are lowercase letters a-z, digits 0-9, the dot and the hyphen."
        ),
        validators=[validate_email_alias],
    )

    is_active = models.BooleanField(default=True)

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        raise NotImplementedError("Solmukohta 2028 does not support Programme V1")
