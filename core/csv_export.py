# encoding: utf-8

import csv

from django.db import models


ENCODING = 'ISO-8859-15'


class CsvExportMixin(object):
    @classmethod
    def get_csv_fields(cls, event):
        fields = []

        for field in cls._meta.fields:
            fields.append((cls, field))

        for field, unused in cls._meta.get_m2m_with_model():
            fields.append((cls, field))

        return fields

    def get_csv_related(self):
        return dict()


def write_header_row(event, writer, fields, m2m_mode='separate_columns'):
    header_row = []

    for (model, field) in fields:
        if type(field) == models.ManyToManyField:
            if m2m_mode == 'separate_columns':
                choices = get_m2m_choices(event, field)
                header_row.extend(
                    u"{field.name}: {choice}"
                    .format(field=field, choice=choice.__unicode__())
                    .encode(ENCODING, 'ignore')
                    for choice in choices
                )
            elif m2m_mode == 'comma_separated':
                header_row.append(field.name)
            else:
                raise NotImplemented(m2m_mode)
        else:
            header_row.append(field.name.encode(ENCODING, 'ignore'))

    writer.writerow(header_row)    


def convert_value(value):
    return unicode(value).encode(ENCODING, 'ignore')


def get_m2m_choices(event, field):
    target_model = field.rel.to

    if any(f.name == 'event' for f in target_model._meta.fields):
        choices = target_model.objects.filter(event=event)
    else:
        choices = target_model.objects.all()

    return choices.order_by('pk')


def write_row(event, writer, fields, model_instance, m2m_mode):
    result_row = []
    related = model_instance.get_csv_related()

    print related

    for model, field in fields:
        if model in related:
            source_instance = related.get(model, None)
        else:
            source_instance = model_instance

        field_value = getattr(source_instance, field.name) if source_instance is not None else None

        if type(field) == models.ManyToManyField and field_value is not None:
            if m2m_mode == 'separate_columns':
                choices = get_m2m_choices(event, field)

                result_row.extend(
                    convert_value(field_value.filter(pk=choice.pk).exists())
                    for choice in choices
                )
            elif m2m_mode == 'comma_separated':
                result_row.append(u', '.join(item.__unicode__() for item in field_value.all()))
            else:
                raise NotImplemented(m2m_mode)
        else:
            result_row.append(convert_value(field_value))

    writer.writerow(result_row)


def export_csv(event, model, model_instances, output_file=None, m2m_mode='separate_columns'):
    fields = model.get_csv_fields(event)

    if output_file is None:
        from cStringIO import StringIO
        string_output = StringIO()
        writer = csv.writer(string_output, dialect='excel-tab')
    else:
        writer = csv.writer(output_file, dialect='excel-tab')

    write_header_row(event, writer, fields, m2m_mode)

    for model_instance in model_instances:
        if isinstance(model_instance, (str, unicode, int)):
            model_instance = model.objects.get(pk=int(model_instances))

        write_row(event, writer, fields, model_instance, m2m_mode)

    if output_file is None:
        result = string_output.getvalue()
        string_output.close()
        return result