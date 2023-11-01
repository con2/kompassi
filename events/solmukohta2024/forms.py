from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import Layout, Fieldset

from core.utils import horizontal_form_helper
from programme.models import AlternativeProgrammeFormMixin, Category, Programme


class ProgrammeForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        admin = kwargs.pop("admin") if "admin" in kwargs else False

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "solmukohta2024_ticket",
            "hosts_from_host",
            "category",
            "title",
            "description",
            "length",
            "solmukohta2024_content_warnings",
            "content_warnings",
            "max_players",
            "solmukohta2024_computer_usage",
            "solmukohta2024_other_needs",
            "solmukohta2024_documentation",
            "solmukohta2024_scheduling",
            "solmukohta2024_panel_participation",
            "solmukohta2024_areas_of_expertise",
            "solmukohta2024_have_you_hosted_before",
            "solmukohta2024_mentoring",
            "notes_from_host",
        )

        self.fields["title"].required = True
        if not admin:
            for field_name in [
                "solmukohta2024_ticket",
                "hosts_from_host",
                "description",
                "length",
                "solmukohta2024_computer_usage",
                "solmukohta2024_documentation",
                "solmukohta2024_have_you_hosted_before",
            ]:
                self.fields[field_name].required = True

        self.fields["category"].queryset = Category.objects.filter(event=event, public=True)

        self.fields["category"].label = _("What type of programme are you suggesting?")
        self.fields["category"].help_text = _(
            "See the Hosting Guide for descriptions of the programme types."
        )

        self.fields["title"].label = _("Name of programme item")
        self.fields["title"].help_text = _(
            "Solmukohta 2024 reserves the right to edit the name for length or clarity."
        )

        self.fields["description"].help_text = _(
            "Please enter the programme description as it should be shown in the programme guide. "
            "Solmukohta 2024 reserves the right to edit the description. "
            "The suggested length is 300 - 500 characters."
        )

        self.fields["length"].help_text = _(
            "Please enter the desired programme length IN MINUTES. "
            "Talks, panels and roundtables should be 45 or 105 minutes in length. "
            "Workshops and larps have a maximum length of 225 minutes including debrief."
        )

        self.fields["content_warnings"].label = _("Other content warnings")
        self.fields["content_warnings"].help_text = _(
            "If your programme item has other content warnings not covered by the choices above, please list them here."
        )

        self.fields["max_players"].label = _("Maximum number of participants")
        self.fields["max_players"].help_text = _(
            "For workshops, larps, roundtables and other programme items with limited attendance, "
            "please enter the maximum number of participants (numeric values only). "
            "If there is a minimum number, put it in the open comment field at the end of this form."
        )

        self.fields["notes_from_host"].help_text = _(
            "If you have anything else to say, this is the place for it!"
        )

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            "solmukohta2024_ticket",
            "hosts_from_host",
            "category",
            "title",
            "description",
            "length",
            "solmukohta2024_content_warnings",
            "content_warnings",
            "max_players",
            "solmukohta2024_computer_usage",
            "solmukohta2024_other_needs",
            "solmukohta2024_documentation",
            "solmukohta2024_scheduling",
            "solmukohta2024_panel_participation",
            "solmukohta2024_areas_of_expertise",
            "solmukohta2024_have_you_hosted_before",
            "solmukohta2024_mentoring",
            "notes_from_host",
        )

        widgets = dict(
            solmukohta2024_content_warnings=forms.CheckboxSelectMultiple,
            solmukohta2024_documentation=forms.CheckboxSelectMultiple,
            solmukohta2024_panel_participation=forms.CheckboxSelectMultiple,
            solmukohta2024_mentoring=forms.CheckboxSelectMultiple,
        )
