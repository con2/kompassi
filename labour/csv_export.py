# encoding: utf-8

import csv

from core.models import Person

from .models import Signup


def get_signup_fields(event):
    signup_fields = []

    models = [Person, Signup]

    SignupExtra = event.labour_event_meta.signup_extra_model
    if SignupExtra is not None:
        models.append(SignupExtra)

    for model in models:
        for field in model._meta.fields:
            signup_fields.append((model, field.name))

    return signup_fields


def export_csv(event, signups, output_file=None):
    fields = get_signup_fields(event)

    header_row = [
        "{model._meta.model_name}.{field_name}".format(model=model, field_name=field_name)
        for (model, field_name) in fields
    ]

    if output_file is None:
        from cStringIO import StringIO
        string_output = StringIO()
        writer = csv.writer(string_output, dialect='excel-tab')
    else:
        writer = csv.writer(output_file, dialect='excel-tab')

    writer.writerow(header_row)

    for signup in signups:
        if type(signup) is not Signup:
            signup = Signup.objects.get(pk=signup)

        result_row = []

        for model, field_name in fields:
            model_instance = model.get_for_signup(signup)

            result_row.append(getattr(model_instance, field_name))

        writer.writerow(result_row)

    if output_file is None:
        result = string_output.getvalue()
        string_output.close()
        return result