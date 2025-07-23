from functools import cached_property

from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, get_code, set_defaults


class AlternativeProgrammeForm(models.Model):
    """
    Most programmes are registered using the default form. However, some programmes are "special",
    such as the role playing games. We would still like to get their programmes, but they need to
    answer a different set of stupid questions.

    This model represents an alternative form that some the hosts of these "special" progammes can
    use to sign up. If you have dabbled with Labour, think of the AlternativeSignupForm.

    Where this differs from AlternativeSignupForm is that we may also choose to publish some of
    these.

    Instances of AlternativeProgrammeForm are supposed to be installed in the database by a setup
    script. For examples, see `hitpoint2017/management/commands/setup_hitpoint2017.py` and look for
    AlternativeProgrammeForm.

    The actual form classes should inherit from django.forms.ModelForm and
    programme.forms.AlternativeFormMixin. For examples, see
    `hitpoint2017/forms.py` and look for RolePlayingGameForm and FreeformProgrammeForm.

    Note that if AlternativeProgrammeForms are specified at all for an event, then if you want to
    allow the default form, also it must be provided as an AlternativeProgrammeForm. If no
    AlternativeProgrammeForms are specified, the default form is used.
    """

    id: int

    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, verbose_name=_("event"))

    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    title = models.CharField(
        max_length=1023,
        verbose_name=_("title"),
        help_text=_("This title is visible to the programme host."),
    )

    description = models.TextField(
        null=True,
        blank=True,
        default="",
        verbose_name=_("description"),
        help_text=_("Visible to the hosts that register their programmes using this form."),
    )

    short_description = models.TextField(
        null=True,
        blank=True,
        default="",
        verbose_name=_("short description"),
        help_text=_("Visible on the page that offers different kinds of forms."),
    )

    programme_form_code = models.CharField(
        max_length=63,
        help_text=_(
            "A reference to the form class that implements the form. Example: hitpoint2017.forms:RolePlayingGameForm"
        ),
    )

    is_active = models.BooleanField(default=True)

    num_extra_invites = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Number of extra invites"),
        help_text=_(
            "To support programmes with multiple hosts, the host offering the programme may be "
            "enabled to invite more hosts to their programme by entering their e-mail addresses. "
            "This field controls if this is available and at most how many e-mail addresses may be "
            "entered."
        ),
    )

    order = models.IntegerField(default=0)

    role = models.ForeignKey(
        "programme.Role",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Role"),
        help_text=_("If set, programme hosts entering programme using this form will by default gain this role."),
    )

    v2_dimensions = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "dimension slug -> list of dimension value slugs. "
            "When program is imported to v2, dimension values indicated here are added to programs of this category."
        ),
    )

    def __str__(self):
        return self.title

    @property
    def qualified_slug(self):
        return f"form-{self.slug}"

    @cached_property
    def programme_form_class(self):
        cp = self.programme_form_code
        if not cp.startswith("kompassi."):
            cp = f"kompassi.{cp}"
        return get_code(cp)

    class Meta:
        verbose_name = _("alternative programme form")
        verbose_name_plural = _("alternative programme forms")
        unique_together = [
            ("event", "slug"),
        ]
        ordering = ("event", "order", "title")


class AlternativeProgrammeFormMixin:
    """
    Stub implementations of required methods for alternative programme form implementations.
    Alternative programme form implementations should inherit from `django.forms.ModelForm` and this
    mixin.

    Part of the alternative programme form facility. For detailed explanation, see the documentation
    of AlternativeProgrammeForm in `programme.models`.
    """

    def get_categories(self, event, admin=False):
        """
        We assume alternative forms do not usually present a programme categories field to the user.
        If this is not the case, override this method to return the programme categories that
        can be applied to.
        """
        from .category import Category

        return Category.objects.filter(event=event, public=True)

    def get_excluded_field_defaults(self):
        return dict()

    def get_excluded_m2m_field_defaults(self):
        return dict()

    def process(self, obj):
        set_defaults(obj, **self.get_excluded_field_defaults())
        obj = self.save()  # type: ignore

        defaults = self.get_excluded_m2m_field_defaults()
        for key, values in defaults:
            manager = getattr(obj, key)
            manager.set(values, clear=True)

        return obj
