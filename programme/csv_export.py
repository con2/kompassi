# encoding: utf-8

import csv

from django.db import models

from core.models import Person
from core.csv_export import write_header_row, write_row, export_csv as core_export_csv

from .models import Programme


def get_programme_fields():
    programme_fields = []

    for field in Programme._meta.fields:
        programme_fields.append((Programme, field))

    for field, unused in Programme._meta.get_m2m_with_model():
        programme_fields.append((Programme, field))

    return programme_fields


def write_programmes(event, writer, fields, programmes):
    for programme in programmes:
        if type(programme) is not Programme:
            programme = Programme.objects.get(pk=programme)

        write_row(event, writer, fields, programme)


def export_csv(event, programmes, output_file=None):
    fields = get_programme_fields()
    return core_export_csv(event, fields, Programme, programmes, output_file, m2m_mode='comma_separated')
