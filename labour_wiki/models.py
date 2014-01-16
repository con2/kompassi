from django.db import models


class LabourWikiSpace(models.Model):
    event = models.ForeignKey('core.Event')
    slug = SlugField()

    space = models.ForeignKey('wiki.Space')

    read_groups = models.ManyToManyField('auth.Group')
    edit_groups = models.ManyToManyField('auth.Group')
