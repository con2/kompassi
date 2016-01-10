# encoding: utf-8

from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from core.models import EventMetaBase
from core.utils import full_hours_between, is_within_period

from .constants import GROUP_VERBOSE_NAMES_BY_SUFFIX, SIGNUP_STATE_GROUPS


class LabourEventMeta(EventMetaBase):
    signup_extra_content_type = models.ForeignKey('contenttypes.ContentType')

    registration_opens = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'työvoimahaku alkaa'
    )

    registration_closes = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'työvoimahaku päättyy'
    )

    work_begins = models.DateTimeField(verbose_name=u'Ensimmäiset työvuorot alkavat')
    work_ends = models.DateTimeField(verbose_name=u'Viimeiset työvuorot päättyvät')

    monitor_email = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'tarkkailusähköposti',
        help_text=u'Kaikki työvoimajärjestelmän lähettämät sähköpostiviestit lähetetään myös '
            u'tähän osoitteeseen.',
    )

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'yhteysosoite',
        help_text=u'Kaikki työvoimajärjestelmän lähettämät sähköpostiviestit lähetetään tästä '
            u'osoitteesta, ja tämä osoite näytetään työvoimalle yhteysosoitteena. Muoto: Selite &lt;osoite@esimerkki.fi&gt;.',
    )

    signup_message = models.TextField(
        null=True,
        blank=True,
        default=u'',
        verbose_name=u'Ilmoittautumisen huomautusviesti',
        help_text=u'Tämä viesti näytetään kaikille työvoimailmoittautumisen alussa. Käytettiin '
            u'esimerkiksi Tracon 9:ssä kertomaan, että työvoimahaku on avoinna enää JV:ille ja '
            u'erikoistehtäville.',
    )

    class Meta:
        verbose_name = _(u'labour event meta')
        verbose_name_plural = _(u'labour event metas')

    def __unicode__(self):
        return self.event.name if self.event else 'None'

    @property
    def signup_extra_model(self):
        return self.signup_extra_content_type.model_class()

    @classmethod
    def events_registration_open(cls):
        from core.models import Event
        t = now()
        return Event.objects.filter(
            laboureventmeta__registration_opens__isnull=False,
            laboureventmeta__registration_opens__lte=t,
        ).exclude(
            laboureventmeta__registration_closes__isnull=False,
            laboureventmeta__registration_closes__lte=t,
        )

    @classmethod
    def get_or_create_dummy(cls):
        from django.contrib.contenttypes.models import ContentType
        from core.models import Event
        from .signup_extras import EmptySignupExtra

        event, unused = Event.get_or_create_dummy()
        content_type = ContentType.objects.get_for_model(EmptySignupExtra)
        admin_group, = LabourEventMeta.get_or_create_groups(event, ['admins'])

        t = now()

        labour_event_meta, created = cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                signup_extra_content_type=content_type,
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
                work_begins=event.start_time - timedelta(days=1),
                work_ends=event.end_time + timedelta(days=1),
                contact_email='dummy@example.com',
                monitor_email='dummy@example.com',
            )
        )

        labour_event_meta.create_groups()

        return labour_event_meta, created

    @classmethod
    def get_or_create_groups(cls, event, job_categories_or_suffixes):
        suffixes = [
            jc_or_suffix if isinstance(jc_or_suffix, basestring) else jc_or_suffix.slug
            for jc_or_suffix in job_categories_or_suffixes
        ]

        groups = super(LabourEventMeta, cls).get_or_create_groups(event, suffixes)

        if 'mailings' in settings.INSTALLED_APPS:
            from mailings.models import RecipientGroup

            for jc_or_suffix, group in zip(job_categories_or_suffixes, groups):
                if isinstance(jc_or_suffix, basestring):
                    verbose_name = GROUP_VERBOSE_NAMES_BY_SUFFIX[jc_or_suffix]
                else:
                    verbose_name = jc_or_suffix.name

                RecipientGroup.objects.get_or_create(
                    event=event,
                    app_label='labour',
                    group=group,
                    defaults=dict(
                        verbose_name=verbose_name,
                    ),
                )

        return groups

    def is_user_supervisor(self, user):
        supervisor_group, = LabourEventMeta.get_or_create_groups(self.event, ['supervisors'])
        return self.is_user_admin(user) or self.is_user_in_group(user, supervisor_group)

    def create_groups(self):
        from .job_category import JobCategory

        job_categories_or_suffixes = list(SIGNUP_STATE_GROUPS)
        job_categories_or_suffixes.extend(JobCategory.objects.filter(event=self.event))
        job_categories_or_suffixes.append('supervisors')
        return LabourEventMeta.get_or_create_groups(self.event, job_categories_or_suffixes)

    @property
    def is_registration_open(self):
        return is_within_period(self.registration_opens, self.registration_closes)

    def is_person_signed_up(self, person):
        return self.event.signup_set.filter(person=person).exists()

    def get_signup_for_person(self, person):
        from .signup import Signup

        try:
            return self.event.signup_set.get(person=person)
        except Signup.DoesNotExist:
            return Signup(person=person, event=self.event)

    @property
    def work_hours(self):
        return full_hours_between(self.work_begins, self.work_ends)

    @property
    def applicants_group(self):
        return self.get_group('applicants')

    @property
    def accepted_group(self):
        return self.get_group('accepted')

    @property
    def finished_group(self):
        return self.get_group('finished')

    @property
    def rejected_group(self):
        return self.get_group('rejected')