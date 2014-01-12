# encoding: utf-8

from django.contrib import admin

from .models import LabourEventMeta


class InlineLabourEventMetaAdmin(admin.StackedInline):
    model = LabourEventMeta
    fields = ('registration_opens', 'registration_closes')