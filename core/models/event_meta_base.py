# encoding: utf-8

from django.db import models

from .group_management_mixin import GroupManagementMixin


class EventMetaBase(models.Model, GroupManagementMixin):
    event = models.OneToOneField('core.Event', on_delete=models.CASCADE, primary_key=True, related_name='%(class)s')
    admin_group = models.ForeignKey('auth.Group', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def get_group(self, suffix):
        from django.contrib.auth.models import Group

        group_name = self.make_group_name(self.event, suffix)

        return Group.objects.get(name=group_name)
