from functools import cached_property

from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils.misc_utils import get_code, set_defaults
from kompassi.core.utils.model_utils import NONUNIQUE_SLUG_FIELD_PARAMS
from kompassi.core.utils.time_utils import is_within_period


class AlternativeSignupForm(models.Model):
    """
    Most workers are registered using the default form. However, some workers are "special",
    such as the organizers (ConCom). We would still like to get their Signups, but they do not
    need to answer all the stupid questions - just some of them.

    This model represents an alternative form that some of these "special" workers can use to sign
    up. Access to this alternative form is controlled using the link. If you know the URL, you can
    use the form.

    Instances of AlternativeSignupForm are supposed to be installed in the database by a setup
    script. For examples, see `tracon9/management/commands/setup_tracon.py` and look for
    AlternativeSignupForm.

    The actual form classes should inherit from django.forms.ModelForm and
    labour.forms.AlternativeFormMixin. For examples, see `tracon9/forms.py` and look for
    OrganizerSignupForm and OrganizerSignupExtraForm.
    """

    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, verbose_name="Tapahtuma")

    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    title = models.CharField(max_length=63, verbose_name="Otsikko", help_text="Tämä otsikko näkyy käyttäjälle.")

    signup_form_class_path = models.CharField(
        max_length=63,
        help_text="Viittaus ilmoittautumislomakkeen toteuttavaan luokkaan. Esimerkki: tracon9.forms:ConcomSignupForm",
    )

    signup_extra_form_class_path = models.CharField(
        max_length=63,
        default="labour.forms:SignupExtraForm",
        help_text="Viittaus lisätietolomakkeen toteuttavaan luokkaan. Esimerkki: tracon9.forms:ConcomSignupExtraForm",
    )

    active_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Active from"),
    )

    active_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Active until"),
    )

    signup_message = models.TextField(
        null=True,
        blank=True,
        default="",
        verbose_name="Ilmoittautumisen huomautusviesti",
        help_text="Tämä viesti näytetään kaikille tätä lomaketta käyttäville työvoimailmoittautumisen alussa. Käytettiin "
        "esimerkiksi Tracon 9:ssä kertomaan, että työvoimahaku on avoinna enää JV:ille ja "
        "erikoistehtäville.",
    )

    def __str__(self):
        return self.title

    @cached_property
    def signup_form_class(self):
        cp = self.signup_form_class_path
        if not cp.startswith("kompassi."):
            cp = f"kompassi.{cp}"

        return get_code(cp)

    @cached_property
    def signup_extra_form_class(self):
        cp = self.signup_extra_form_class_path
        if not cp.startswith("kompassi."):
            cp = f"kompassi.{cp}"

        return get_code(cp)

    @property
    def is_active(self):
        return is_within_period(self.active_from, self.active_until)

    class Meta:
        verbose_name = _("alternative signup form")
        verbose_name_plural = _("alternative signup forms")
        unique_together = [
            ("event", "slug"),
        ]


class AlternativeFormMixin:
    """
    Stub implementations of required methods for alternative signup form implementations.
    Alternative signup form implementations should inherit from `django.forms.ModelForm` and this
    mixin.

    Part of the alternative signup form facility. For detailed explanation, see the documentation
    of AlternativeSignupForm in `labour.models`.
    """

    def get_job_categories(self, event, admin=False):
        """
        We assume alternative forms do not usually present a job categories field to the user.
        If this is not the case, override get_job_categories to return the job categories that
        can be applied to. For a default implementation, consult SignupForm.
        """
        from .job_category import JobCategory

        return JobCategory.objects.none()

    def get_excluded_field_defaults(self):
        return dict()

    def get_excluded_m2m_field_defaults(self):
        return dict()

    def process(self, obj):
        set_defaults(obj, **self.get_excluded_field_defaults())
        obj = self.save()  # type: ignore

        defaults = self.get_excluded_m2m_field_defaults()
        for key, values in defaults.items():
            manager = getattr(obj, key)
            manager.set(values)

        return obj
