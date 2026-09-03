from typing import Self

from django import forms as django_forms

from kompassi.core.utils.form_utils import camel_case_keys_to_snake_case
from kompassi.core.utils.retention_period import days_to_timedelta

from ...models.registry import Registry


class RegistryForm(django_forms.ModelForm):
    default_retention_period_days = django_forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = Registry
        fields = (
            # NOTE SUPPORTED_LANGUAGES
            "title_en",
            "title_fi",
            "title_sv",
            "policy_url_en",
            "policy_url_fi",
            "policy_url_sv",
        )

    @classmethod
    def from_form_data(cls, instance: Registry | None, form_data: dict[str, str], **kwargs) -> Self:
        form_data = camel_case_keys_to_snake_case(form_data)
        return cls(form_data, instance=instance, **kwargs)

    def save(self, commit: bool = True) -> Registry:
        registry = super().save(commit=False)
        registry.default_retention_period = days_to_timedelta(self.cleaned_data.get("default_retention_period_days"))
        if commit:
            registry.save()
        return registry
