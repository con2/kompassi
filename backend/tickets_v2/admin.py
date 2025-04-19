"""
NOTE: Generally V2 apps should not rely on taka-admin to do basic administrative tasks.
This should be thought of an escape hatch and most admin functions provided in etuadmin.
"""

from django import forms
from django.contrib import admin

from .models.meta import TicketsV2EventMeta


class TicketsV2EventMetaForm(forms.ModelForm):
    class Meta:
        model = TicketsV2EventMeta
        fields = (
            "contact_email",
            "provider_id",
            # NOTE SUPPORTED_LANGUAGES
            "terms_and_conditions_url_en",
            "terms_and_conditions_url_fi",
            "terms_and_conditions_url_sv",
        )
        widgets = dict(
            terms_and_conditions_url_en=forms.TextInput,
            terms_and_conditions_url_fi=forms.TextInput,
            terms_and_conditions_url_sv=forms.TextInput,
        )


class InlineTicketsV2EventMetaAdmin(admin.StackedInline):
    model = TicketsV2EventMeta
    form = TicketsV2EventMetaForm
