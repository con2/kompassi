# encoding: utf-8

from collections import namedtuple
from itertools import cycle

from django.db import models
from django.db.models import Q
from django.utils.html import escape
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from core.csv_export import CsvExportMixin
from core.models import EventMetaBase
from core.utils import slugify, NONUNIQUE_SLUG_FIELD_PARAMS, time_bool_property, code_property
from labour.models import PersonnelClass


BADGE_ELIGIBLE_FOR_BATCHING = dict(
    batch__isnull=True,
    printed_separately_at__isnull=True,
    revoked_at__isnull=True,
)


class Progress(object):
    __slots__ = [
        'css_class',
        'max',
        'text',
        'value',
        'width',
        'inflated',
    ]
    from core.utils import simple_object_init as __init__
    from core.utils import simple_object_repr as __repr__


PROGRESS_ELEMENT_MIN_WIDTH = 4 # %


class CountBadgesMixin(object):
    def count_printed_badges(self):
        return self.badge_set.filter(
            Q(batch__isnull=False, batch__printed_at__isnull=False) | Q(printed_separately_at__isnull=False)
        ).distinct().count()

    def count_badges_waiting_in_batch(self):
        return self.badge_set.filter(batch__isnull=False, batch__printed_at__isnull=True, revoked_at__isnull=True).count()

    def count_badges_awaiting_batch(self):
        return self.badge_set.filter(**BADGE_ELIGIBLE_FOR_BATCHING).count()

    def count_badges(self):
        return self.badge_set.count()

    def count_revoked_badges(self):
        return self.badge_set.filter(revoked_at__isnull=False).count()

    def get_progress(self):
        """
        We build a progress bar widget that shows percentages of badges in different states.
        However, if the percentage is really small, the progress segment in the progress bar
        would get too small. We account for that by "inflating" segments that are too small,
        and "deflating" segments that are big enough so that taking away some of their width
        does not cause a signicifant error in their relative sizes.

        TODO: This method should be generalized to work with all kinds of multi-segment
        progress bars, not just this particular occasion.
        """
        progress = []

        pb_max = self.count_badges()
        percentace_consumed_for_inflation = 0

        for pb_class, pb_text, pb_value in [
            ('progress-bar-success', u'Tulostettu', self.count_printed_badges()),
            ('progress-bar-danger', u'Mitätöity', self.count_revoked_badges()),
            ('progress-bar-info', u'Odottaa erässä', self.count_badges_waiting_in_batch()),
            ('progress-bar-grey', u'Odottaa erää', self.count_badges_awaiting_batch()),
        ]:

            if pb_value > 0:
                width = 100.0 * pb_value / max(pb_max, 1)
                width = int(width + 0.5)

                if width < PROGRESS_ELEMENT_MIN_WIDTH:
                    percentace_consumed_for_inflation += PROGRESS_ELEMENT_MIN_WIDTH - width
                    width = PROGRESS_ELEMENT_MIN_WIDTH
                    inflated = True
                else:
                    inflated = False

                progress.append(Progress(
                    css_class=pb_class,
                    max=pb_max,
                    text=pb_text,
                    value=pb_value,
                    width=width,
                    inflated=inflated,
                ))

        if sum(p.width for p in progress) > 100:
            candidates_for_deflation = [p for p in progress if p.width > PROGRESS_ELEMENT_MIN_WIDTH]
            candidates_for_deflation.sort(key=lambda p: -p.width)

            for p in cycle(candidates_for_deflation):
                if (
                    sum(p.width for p in progress) <= 100 or
                    all(p.width <= PROGRESS_ELEMENT_MIN_WIDTH for p in candidates_for_deflation)
                ):
                    break

                if p.width > PROGRESS_ELEMENT_MIN_WIDTH:
                    p.width -= 1
                    percentace_consumed_for_inflation -= 1

        # FIXME sometime this assert blows
        #assert sum(p.width for p in progress) in [100, 0], "Missing percentage"

        return progress



class BadgesEventMeta(EventMetaBase, CountBadgesMixin):
    badge_factory_code = models.CharField(
        max_length=255,
        default='badges.utils:default_badge_factory',
        verbose_name=u'Badgetehdas',
        help_text=u'Funktio, joka selvittää, minkä tyyppinen badge henkilölle pitäisi luoda. '
            u'Oletusarvo toimii lähes kaikille tapahtumille.'
    )

    badge_factory = code_property('badge_factory_code')
    badge_layout = models.CharField(
        max_length=4,
        default='trad',
        choices=(('trad', u'Perinteinen'), ('nick', u'Nickiä korostava')),
        verbose_name=u'Badgen asettelu',
        help_text=u'Perinteinen: tehtävänimike, etunimi sukunimi, nick. Nickiä korostava: nick tai etunimi, sukunimi tai koko nimi, tehtävänimike.',
    )

    real_name_must_be_visible = models.BooleanField(
        default=False,
        verbose_name=_(u'Require real name to be visible'),
        help_text=_(
            u'In most events, it is up to the person carrying the badge to decide whether or not '
            u'their real name is displayed in their badge. Some choose to go by their first name or nick '
            u'name only. Some events have, however, decided to restrict this and require the first name and '
            u'surname to be visible in all badges. If this option is selected, only the name display styles '
            u'<em>Firstname Surname</em> and <em>Firstname "Nick" Surname</em> are effectively allowed.'
        )
    )

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        group, = cls.get_or_create_groups(event, ['admins'])
        return cls.objects.get_or_create(event=event, defaults=dict(admin_group=group))

    # for CountBadgesMixin
    @property
    def badge_set(self):
        return Badge.objects.filter(personnel_class__event=self.event)


class Batch(models.Model, CsvExportMixin):
    event = models.ForeignKey('core.Event', related_name='badge_batch_set')

    personnel_class = models.ForeignKey(PersonnelClass, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Luotu')
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u'Päivitetty')
    printed_at = models.DateTimeField(null=True, blank=True)

    is_printed = time_bool_property('printed_at')

    @classmethod
    def create(cls, event, personnel_class=None, max_items=100):
        if personnel_class is not None:
            assert personnel_class.event == event
            badges = Badge.objects.filter(personnel_class=personnel_class)
        else:
            badges = Badge.objects.filter(personnel_class__event=event)

        badges = badges.filter(**BADGE_ELIGIBLE_FOR_BATCHING).order_by('created_at')

        if max_items is not None:
            badges = badges[:max_items]

        batch = cls(personnel_class=personnel_class, event=event)
        batch.save()

        # Cannot update a query once a slice has been taken.
        # badges.update(batch=batch)
        for badge in badges:
            badge.batch = batch
            badge.save()

        return batch

    def confirm(self):
        self.printed_at = now()
        self.save()

    def cancel(self):
        self.badge_set.update(batch=None)
        self.delete()

    def can_cancel(self):
        return self.printed_at is not None

    def can_confirm(self):
        return self.printed_at is not None

    def __unicode__(self):
        return u"Tulostuserä {}".format(self.pk)


class Badge(models.Model):
    person = models.ForeignKey('core.Person', null=True, blank=True)

    personnel_class = models.ForeignKey(PersonnelClass, null=True, blank=True, verbose_name=u'Henkilöstöluokka')

    printed_separately_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    job_title = models.CharField(max_length=63, blank=True, default=u'', verbose_name=u'Tehtävänimike')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Luotu')
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u'Päivitetty')

    batch = models.ForeignKey(Batch, null=True, blank=True, db_index=True)

    is_revoked = time_bool_property('revoked_at')
    is_printed = time_bool_property('printed_at')
    is_printed_separately = time_bool_property('printed_separately_at')

    @property
    def printed_at(self):
        if self.batch:
            return self.batch.printed_at
        else:
            return self.printed_separately_at

    @property
    def formatted_printed_at(self):
        # XXX not really "formatted"
        return self.printed_at if self.printed_at is not None else u''

    @classmethod
    def get_or_create_dummy(cls):
        person, unused = Person.get_or_create_dummy()
        personnel_class, unused = PersonnelClass.get_or_create_dummy()

        return cls.objects.get_or_create(
            person=person,
            personnel_class=personnel_class,
        )

    @classmethod
    def get_or_create(cls, event, person):
        # FIXME If someone first does programme and then labour, they should still get labour badge.
        # Factory should be invoked anyway, and badge "upgraded" (revoke old, create new).

        try:
            return cls.objects.get(personnel_class__event=event, person=person), False
        except cls.DoesNotExist:
            factory = event.badges_event_meta.badge_factory

            badge_opts = factory(event=event, person=person)
            badge_opts = dict(badge_opts, person=person)

            badge = cls(**badge_opts)
            badge.save()

            return badge, True

    @classmethod
    def get_csv_fields(cls, event):
        meta = event.badges_event_meta
        if meta.badge_layout == 'trad':
            # Chief Technology Officer
            # Santtu Pajukanta
            # Japsu
            return [
                (PersonnelClass, 'slug'),
                (cls, 'surname'),
                (cls, 'first_name'),
                (cls, 'nick'),
                (cls, 'job_title'),
            ]
        elif meta.badge_layout == 'nick':
            # JAPSU
            # Santtu Pajukanta
            # Chief Technology Officer
            # -OR-
            # SANTTU
            # Pajukanta
            # Chief Technology Officer
            return [
                (cls, 'personnel_class_name'),
                (cls, 'nick_or_first_name'),
                (cls, 'surname_or_full_name'),
                (cls, 'job_title'),
            ]
        else:
            raise NotImplementedError(meta.badge_layout)

    def get_csv_related(self):
        from core.models import Person

        return {
            PersonnelClass: self.personnel_class,
            Person: self.person,
        }

    def get_name_fields(self):
        return [
            (self.person.surname.strip(), self.is_surname_visible),
            (self.person.first_name.strip(), self.is_first_name_visible),
            (self.person.nick.strip(), self.is_nick_visible),
        ]

    @property
    def personnel_class_name(self):
        return self.personnel_class.name if self.personnel_class else u''

    @property
    def event(self):
        return self.personnel_class.event

    @property
    def meta(self):
        return self.event.badges_event_meta

    @property
    def event_name(self):
        return self.personnel_class.event.name if self.personnel_class else u''

    @property
    def person_full_name(self):
        return self.person.full_name if self.person else u''

    @property
    def first_name(self):
        return self.person.first_name.strip() if self.is_first_name_visible else u''

    @property
    def is_first_name_visible(self):
        return self.meta.real_name_must_be_visible or self.person.is_first_name_visible

    @property
    def nick_or_first_name(self):
        if self.is_nick_visible:
            # JAPSU <- this
            # Santtu Pajukanta
            # Chief Technology Officer
            return self.person.nick
        elif self.is_first_name_visible:
            # SANTTU <- this
            # Pajukanta
            # Chief Technology Officer
            return self.person.first_name
        else:
            # NOTE we do not offer a choice of showing the surname but not the first name
            raise NotImplementedError(self.person.name_display_style)

    @property
    def surname(self):
        return self.person.surname.strip() if self.is_surname_visible else u''

    @property
    def is_surname_visible(self):
        return self.meta.real_name_must_be_visible or self.person.is_surname_visible

    @property
    def surname_or_full_name(self):
        if self.is_nick_visible:
            # JAPSU
            # Santtu Pajukanta <- this
            # Chief Technology Officer
            if self.is_surname_visible:
                if self.is_first_name_visible:
                    return u"{first_name} {surname}".format(
                        first_name=self.person.first_name,
                        surname=self.person.surname,
                    )
                else:
                    # NOTE we do not offer a choice of showing the surname but not the first name
                    raise NotImplementedError(self.person.name_display_style)
            else:
                return u''
        else:
            # SANTTU
            # Pajukanta <- this
            # Chief Technology Officer
            if self.is_surname_visible:
                return self.person.surname
            else:
                return u''

    @property
    def nick(self):
        return self.person.nick.strip() if self.is_nick_visible else u''

    @property
    def is_nick_visible(self):
        return self.person.is_nick_visible

    def to_html_print(self):
        def format_name_field(value, is_visible):
            if is_visible:
                return u"<strong>{value}</strong>".format(value=escape(value))
            else:
                return escape(value)

        vars = dict(
            surname=format_name_field(self.person.surname.strip(), self.is_surname_visible),
            first_name=format_name_field(self.person.first_name.strip(), self.is_first_name_visible),
            nick=format_name_field(self.person.nick.strip(), self.is_nick_visible),
        )

        if self.person.nick:
            return u"{surname}, {first_name}, {nick}".format(**vars)
        else:
            return u"{surname}, {first_name}".format(**vars)

    def __unicode__(self):
        return u"{person_name} ({personnel_class_name}, {event_name})".format(
            person_name=self.person_full_name,
            personnel_class_name=self.personnel_class_name,
            event_name=self.event_name,
        )
