from django.db import models


class SimpleChoice(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class ContentWarning(SimpleChoice):
    pass


class Documentation(SimpleChoice):
    pass


class PanelParticipation(SimpleChoice):
    pass


class Mentoring(SimpleChoice):
    pass


class Technology(SimpleChoice):
    pass
