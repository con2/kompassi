# encoding: utf-8

import csv

from django.db import models

from core.models import Person
from core.csv_export import write_header_row, write_row, export_csv as core_export_csv

from .models import Signup


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


def write_signups(event, writer, fields, signups):
    for signup in signups:
        if type(signup) is not Signup:
            signup = Signup.objects.get(pk=signup)

        write_row(event, writer, fields, signup)


def export_csv(event, signups, output_file=None):
    fields = get_signup_fields(event)
    return core_export_csv(event, fields, Signup, signups, output_file)
