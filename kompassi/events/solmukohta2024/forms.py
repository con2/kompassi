from crispy_forms.layout import Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import horizontal_form_helper
from kompassi.zombies.programme.models import AlternativeProgrammeFormMixin, Category, Programme


class ProgrammeForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        admin = kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "solmukohta2024_ticket",
            "hosts_from_host",
            "solmukohta2024_other_emails",
            "category",
            "title",
            "description",
            "length_from_host",
            "solmukohta2024_content_warnings",
            "content_warnings",
            "max_players",
            "solmukohta2024_technology",
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
                "length_from_host",
                "solmukohta2024_documentation",
            ]:
                self.fields[field_name].required = True

        self.fields["category"].queryset = Category.objects.filter(event=event, public=True)

        self.fields["category"].label = _("What type of programme are you suggesting?")
        self.fields["category"].help_text = _("See the Hosting Guide for descriptions of the programme types.")

        self.fields["title"].label = _("Name of programme item")
        self.fields["title"].help_text = _("Solmukohta 2024 reserves the right to edit the name for length or clarity.")

        # prevent translation; single translated label looks funny
        self.fields["description"].label = "Description"
        self.fields["notes_from_host"].label = "Anything else?"

        self.fields["description"].help_text = _(
            "Please enter the programme description as it should be shown in the programme guide. "
            "Solmukohta 2024 reserves the right to edit the description. "
            "The suggested length is 300 - 500 characters."
        )

        self.fields["length_from_host"].help_text = _("Programme length")
        self.fields["length_from_host"].help_text = _(
            "How long should your item be? Please note that each programme slot ends at "
            "least 15 minutes before the next slot begins. (So a 1-hour slot is 45 minutes, "
            "a 2-hour one is 105 minutes, and so on. We suggest larps and workshops have a "
            "maximum of 3:45 including debrief. One-hour room parties, however, are a whole "
            "hour!)"
        )

        self.fields["content_warnings"].label = _("Other content warnings")
        self.fields["content_warnings"].help_text = _(
            "If your programme item has other content warnings not covered by the choices "
            "above (depictions of or references to violence, etc.), please list them here. "
            "See the Guide to Hosting Programme for more info."
        )

        self.fields["max_players"].label = _("Maximum number of participants")
        self.fields["max_players"].help_text = _(
            "What’s the maximum number of participants? (If unlimited, leave this blank.)",
        )

        self.fields["notes_from_host"].help_text = _("If you have anything else to say, this is the place for it!")

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            "solmukohta2024_ticket",
            "hosts_from_host",
            "solmukohta2024_other_emails",
            "category",
            "title",
            "description",
            "length_from_host",
            "solmukohta2024_content_warnings",
            "content_warnings",
            "max_players",
            "solmukohta2024_technology",
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
            solmukohta2024_technology=forms.CheckboxSelectMultiple,
            solmukohta2024_content_warnings=forms.CheckboxSelectMultiple,
            solmukohta2024_documentation=forms.CheckboxSelectMultiple,
            solmukohta2024_panel_participation=forms.CheckboxSelectMultiple,
            solmukohta2024_mentoring=forms.CheckboxSelectMultiple,
        )


class AForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "aweek2024_when",
            "long_description",
            "description",
            "length_from_host",
            "aweek2024_participants",
            "content_warnings",
            "aweek2024_signup",
            "aweek2024_prepare",
            "notes_from_host",
        )

        # disable translations
        self.fields["title"].label = "Title"
        self.fields[
            "title"
        ].help_text = "Make up a concise title for your programme. We reserve the right to edit the title."

        self.fields["description"].label = "Description"
        self.fields["notes_from_host"].label = "Anything else?"

        self.fields["long_description"].label = "What do you want to organize?"
        self.fields["long_description"].help_text = "Describe your programme item to us."

        self.fields["description"].help_text = "Public description of your programme item."

        self.fields["length_from_host"].label = "Length of the program item?"
        self.fields["length_from_host"].help_text = None

        self.fields["content_warnings"].label = "Trigger warnings"
        self.fields["content_warnings"].help_text = None

        self.fields["notes_from_host"].help_text = "Anything else you would like to say?"

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="solmukohta2024", slug="aweek-program"),
        )

    class Meta:
        model = Programme
        fields = (
            "title",
            "aweek2024_when",
            "long_description",
            "description",
            "length_from_host",
            "aweek2024_participants",
            "content_warnings",
            "aweek2024_signup",
            "aweek2024_prepare",
            "notes_from_host",
        )

        widgets = dict(
            solmukohta2024_technology=forms.CheckboxSelectMultiple,
            solmukohta2024_content_warnings=forms.CheckboxSelectMultiple,
            solmukohta2024_documentation=forms.CheckboxSelectMultiple,
            solmukohta2024_panel_participation=forms.CheckboxSelectMultiple,
            solmukohta2024_mentoring=forms.CheckboxSelectMultiple,
        )
