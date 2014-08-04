# encoding: utf-8

import csv

from django.db import models


ENCODING = 'ISO-8859-15'


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

    for model, field in fields:
        source_instance = model.csv_get_for_obj(model_instance) if hasattr(model, 'csv_get_for_obj') else model_instance
        field_value = getattr(source_instance, field.name)

        if type(field) == models.ManyToManyField:
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


def export_csv(event, fields, model, model_instances, output_file, m2m_mode='separate_columns'):
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