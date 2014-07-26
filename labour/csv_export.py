# encoding: utf-8

import csv

from django.db import models

from core.models import Person

from .models import Signup


ENCODING = 'ISO-8859-15'


def get_signup_fields(event):
    signup_fields = []

    models = [Person, Signup]

    SignupExtra = event.labour_event_meta.signup_extra_model
    if SignupExtra is not None:
        models.append(SignupExtra)

    for model in models:
        for field in model._meta.fields:
            signup_fields.append((model, field))

        for field, unused in model._meta.get_m2m_with_model():
            signup_fields.append((model, field))

    return signup_fields


def get_m2m_choices(event, field):
    target_model = field.rel.to

    if any(f.name == 'event' for f in target_model._meta.fields):
        choices = target_model.objects.filter(event=event)
    else:
        choices = target_model.objects.all()

    return choices.order_by('pk')


def convert_value(value):
    return unicode(value).encode(ENCODING, 'ignore')


def write_header_row(event, writer, fields):
    header_row = []

    for (model, field) in fields:
        if type(field) == models.ManyToManyField:
            choices = get_m2m_choices(event, field)
            header_row.extend(
                u"{field.name}: {choice}"
                .format(field=field, choice=choice.__unicode__())
                .encode(ENCODING, 'ignore')
                for choice in choices
            )
        else:
            header_row.append(field.name.encode(ENCODING, 'ignore'))

    writer.writerow(header_row)    


def write_signups(event, writer, fields, signups):
    for signup in signups:
        if type(signup) is not Signup:
            signup = Signup.objects.get(pk=signup)

        result_row = []

        for model, field in fields:
            model_instance = model.get_for_signup(signup)
            field_value = getattr(model_instance, field.name)

            if type(field) == models.ManyToManyField:
                choices = get_m2m_choices(event, field)

                result_row.extend(
                    convert_value(field_value.filter(pk=choice.pk).exists())
                    for choice in choices
                )
            else:
                result_row.append(convert_value(field_value))

        writer.writerow(result_row)


def export_csv(event, signups, output_file=None):
    fields = get_signup_fields(event)

    if output_file is None:
        from cStringIO import StringIO
        string_output = StringIO()
        writer = csv.writer(string_output, dialect='excel-tab')
    else:
        writer = csv.writer(output_file, dialect='excel-tab')

    write_header_row(event, writer, fields)
    write_signups(event, writer, fields, signups)

    if output_file is None:
        result = string_output.getvalue()
        string_output.close()
        return result