# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, is_within_period


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

    event = models.ForeignKey('core.Event', verbose_name=u'Tapahtuma')

    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    title = models.CharField(
        max_length=63,
        verbose_name=u'Otsikko',
        help_text=u'Tämä otsikko näkyy käyttäjälle.'
    )

    signup_form_class_path = models.CharField(
        max_length=63,
        help_text=u'Viittaus ilmoittautumislomakkeen toteuttavaan luokkaan. Esimerkki: tracon9.forms:ConcomSignupForm',
    )

    signup_extra_form_class_path = models.CharField(
        max_length=63,
        default='labour.forms:EmptySignupExtraForm',
        help_text=u'Viittaus lisätietolomakkeen toteuttavaan luokkaan. Esimerkki: tracon9.forms:ConcomSignupExtraForm',
    )

    active_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Käyttöaika alkaa',
    )

    active_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Käyttöaika päättyy',
    )

    signup_message = models.TextField(
        null=True,
        blank=True,
        default=u'',
        verbose_name=u'Ilmoittautumisen huomautusviesti',
        help_text=u'Tämä viesti näytetään kaikille tätä lomaketta käyttäville työvoimailmoittautumisen alussa. Käytettiin '
            u'esimerkiksi Tracon 9:ssä kertomaan, että työvoimahaku on avoinna enää JV:ille ja '
            u'erikoistehtäville.',
    )

    def __unicode__(self):
        return self.title

    @property
    def signup_form_class(self):
        if not getattr(self, '_signup_form_class', None):
            from core.utils import get_code
            self._signup_form_class = get_code(self.signup_form_class_path)

        return self._signup_form_class

    @property
    def signup_extra_form_class(self):
        if not getattr(self, '_signup_extra_form_class', None):
            from core.utils import get_code
            self._signup_extra_form_class = get_code(self.signup_extra_form_class_path)

        return self._signup_extra_form_class

    @property
    def is_active(self):
        return is_within_period(self.active_from, self.active_until)

    class Meta:
        verbose_name = _(u'alternative signup form')
        verbose_name_plural = _(u'alternative signup forms')
        unique_together = [
            ('event', 'slug'),
        ]


class AlternativeFormMixin(object):
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