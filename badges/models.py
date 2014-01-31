from django.db import models


class BadgesEventMeta(EventMetaBase):
    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        return cls.get_or_create(event=event)

class Template(models.Model):
    event = models.ForeignKey('core.Event')
    affiliation = models.CharField(max_length=31)


class Badge(models.Model):
    person = models.ForeignKey('core.Person', null=True, blank=True)
    template = models.ForeignKey(Template)
    badge_text = models.CharField(max_length=1023)
    printed_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.person and self.template and not self.badge_text:
            self.badge_text = u"{affiliation}\n{full_name}".format(
                affiliation=self.template.name,
                full_name=self.person.full_name,
            )

        return super(Badge, self).save(*args, **kwargs)

    @classmethod
    def get_or_create_dummy(cls):
        person, unused = Person.get_or_create_dummy()
        template, unused = Template.get_or_create_dummy()

        return cls.objects.get_or_create(
            person=person,
            template=template,
        )