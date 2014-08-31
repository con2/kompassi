# encoding: utf-8

from django.db import models
from django.utils.timezone import now

from core.csv_export import CsvExportMixin
from core.models import EventMetaBase
from core.utils import slugify, NONUNIQUE_SLUG_FIELD_PARAMS, time_bool_property


class BadgesEventMeta(EventMetaBase):
    badge_factory_code = models.CharField(
        max_length='255',
        default='badges.utils:default_badge_factory',
        verbose_name=u'Badgetehdas',
        help_text=u'Funktio, joka selvittää, minkä tyyppinen badge henkilölle pitäisi luoda. '
            u'Oletusarvo toimii, jos tapahtumalla on tasan yksi badgepohja. Ks. esimerkkitoteutus '
            u'tracon9/badges.py:badge_factory.',
    )

    @property
    def badge_factory(self):
        from core.utils import get_code
        return get_code(self.badge_factory_code)

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        group, unused = cls.get_or_create_group(event, 'admins')
        return cls.objects.get_or_create(event=event, defaults=dict(admin_group=group))


class Template(models.Model):
    event = models.ForeignKey('core.Event')
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    name = models.CharField(max_length=63)

    @classmethod
    def get_or_create_dummy(cls):
        meta, unused = BadgesEventMeta.get_or_create_dummy()

        return cls.objects.get_or_create(
            event=meta.event,
            name=u'Dummy badge',
            slug=u'dummy-badge',
        )

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super(Template, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Badgepohja'
        verbose_name_plural = u'Badgepohjat'

        unique_together = [
            ('event', 'slug'),
        ]


class Batch(models.Model, CsvExportMixin):
    event = models.ForeignKey('core.Event', related_name='badge_batch_set')
    template = models.ForeignKey(Template, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Luotu')
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u'Päivitetty')
    printed_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def create(cls, event, template=None, max_badges=100):
        if template is not None:
            assert template.event == event
            badges = Badge.objects.filter(template=template)
        else:
            badges = Badge.objects.filter(template__event=event)

        badges = badges.filter(
            batch__isnull=True,
            printed_separately_at__isnull=True
        ).order_by('created_at')

        if max_badges is not None:
            badges = badges[:max_badges]

        batch = cls(template=template, event=event)
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
    template = models.ForeignKey(Template)
    printed_separately_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    job_title = models.CharField(max_length=63, blank=True, default=u'')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Luotu')
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u'Päivitetty')

    is_revoked = time_bool_property('revoked_at')
    is_printed = time_bool_property('printed_at')

    batch = models.ForeignKey(Batch, null=True, blank=True, db_index=True)

    @property
    def printed_at(self):
        if self.batch:
            return self.batch.printed_at
        else:
            return self.printed_separately_at

    @classmethod
    def get_or_create_dummy(cls):
        person, unused = Person.get_or_create_dummy()
        template, unused = Template.get_or_create_dummy()

        return cls.objects.get_or_create(
            person=person,
            template=template,
        )

    @classmethod
    def get_or_create(cls, event, person):
        # FIXME If someone first does programme and then labour, they should still get labour badge.
        # Factory should be invoked anyway, and badge "upgraded" (revoke old, create new).

        try:
            return False, cls.objects.get(template__event=event, person=person)
        except cls.DoesNotExist:
            factory = event.badges_event_meta.badge_factory

            badge_opts = factory(event=event, person=person)
            badge_opts = dict(badge_opts, person=person)

            badge = cls(**badge_opts)
            badge.save()

            return True, badge

    @classmethod
    def get_csv_fields(cls, *args, **kwargs):
        from core.models import Person

        return [
            (Template, 'slug'),
            (Person, 'surname'),
            (Person, 'first_name'),
            (cls, 'job_title'),
        ]

    def get_csv_related(self):
        return {
            Template: self.template,
            Person: self.person,
        }

    @property
    def name_fields(self):
        return [
            (self.person.first_name, self.person.is_first_name_visible),
            (self.person.surname, self.person.is_surname_visible),
            (self.person.nick, self.person.is_nick_visible),
        ]
