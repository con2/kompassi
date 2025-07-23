from django import forms
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import horizontal_form_helper


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label=_("Search term"),
        help_text=_("Searchable fields: first name, last name, e-mail address, phone number, nick name, user name"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
