# encoding: utf-8



from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, is_within_period, set_defaults, set_attrs


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

    event = models.ForeignKey('core.Event', on_delete=models.CASCADE, verbose_name=_('event'))

    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    title = models.CharField(
        max_length=63,
        verbose_name=_('title'),
        help_text=_('This title is visible to the programme host.'),
    )

    description = models.TextField(
        null=True,
        blank=True,
        default='',
        verbose_name=_('description'),
        help_text=_('Visible to the hosts that register their programmes using this form.'),
    )

    short_description = models.TextField(
        null=True,
        blank=True,
        default='',
        verbose_name=_('short description'),
        help_text=_('Visible on the page that offers different kinds of forms.'),
    )

    programme_form_code = models.CharField(
        max_length=63,
        help_text=_('A reference to the form class that implements the form. Example: hitpoint2017.forms:RolePlayingGameForm'),
    )

    active_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Active from'),
    )

    active_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Active until'),
    )

    num_extra_invites = models.PositiveIntegerField(
        default=5,
        verbose_name=_('Number of extra invites'),
        help_text=_(
            'To support programmes with multiple hosts, the host offering the programme may be '
            'enabled to invite more hosts to their programme by entering their e-mail addresses. '
            'This field controls if this is available and at most how many e-mail addresses may be '
            'entered.'
        )
    )

    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def programme_form_class(self):
        if not getattr(self, '_programme_form_class', None):
            from core.utils import get_code
            self._programme_form_class = get_code(self.programme_form_code)

        return self._programme_form_class

    @property
    def is_active(self):
        return is_within_period(self.active_from, self.active_until)

    @classmethod
    def get_active_alternative_programme_forms(cls, t=None, **kwargs):
        if t is None:
            t = now()

        q = (
            # starting time is defined and it has been passed
            Q(active_from__isnull=False, active_from__lte=t) &

            # if ending time is defined, it must not yet have been passed
            ~Q(active_until__isnull=False, active_until__lte=t)
        )

        if kwargs:
            # any extra criteria that may have been defined
            q = q & Q(**kwargs)

        return cls.objects.filter(q)

    class Meta:
        verbose_name = _('alternative programme form')
        verbose_name_plural = _('alternative programme forms')
        unique_together = [
            ('event', 'slug'),
        ]
        ordering = ('event', 'order', 'title')


class AlternativeProgrammeFormMixin(object):
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
        raise NotImplementedError(
            'At least `category` must be specified unless a category field is included in the form. '
            'In that case, override get_excluded_field_defaults to return a dict (might be empty.)'
        )

    def get_excluded_m2m_field_defaults(self):
        return dict()

    def process(self, obj):
        set_defaults(obj, **self.get_excluded_field_defaults())
        obj = self.save()

        defaults = self.get_excluded_m2m_field_defaults()
        for key, values in defaults:
            manager = getattr(obj, key)
            manager.set(values, clear=True)

        return obj
