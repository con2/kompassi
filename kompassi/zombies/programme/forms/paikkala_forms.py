from django import forms
from django.utils.translation import gettext_lazy as _
from paikkala.forms import ReservationForm as PaikkalaReservationForm
from paikkala.models import Program as PaikkalaProgram

from kompassi.core.utils import horizontal_form_helper

from ..models import Programme


class IsUsingPaikkalaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        disabled = kwargs.pop("disabled")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        if disabled:
            self.fields["is_using_paikkala"].disabled = True

    class Meta:
        fields = ("is_using_paikkala",)
        model = Programme


class PaikkalaProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        # make form texts translatable
        self.fields["reservation_start"].label = _("Reservation start")
        self.fields["reservation_end"].label = _("Reservation end")
        self.fields["reservation_end"].help_text = _(
            "Both reservation start and reservation end must be set for the reservation to be considered open."
        )
        self.fields["invalid_after"].label = _("Invalid after")
        # self.fields['require_user'].label = _('Require user')
        self.fields["max_tickets_per_user"].label = _("Max tickets per user")
        self.fields["max_tickets_per_batch"].label = _("Max tickets per batch")

    class Meta:
        fields = (
            "reservation_start",
            "reservation_end",
            "invalid_after",
            # 'require_user',
            "max_tickets_per_user",
            "max_tickets_per_batch",
        )
        model = PaikkalaProgram


class ReservationForm(PaikkalaReservationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # make these translatable
        self.fields["zone"].label = _("Zone")
        self.fields["zone"].label_format = _("{zone} – {remaining} seats remain")
        self.fields["count"].label = _("Count")
        self.fields["count"].help_text = _("You can reserve at most {max_tickets} tickets.").format(
            max_tickets=self.instance.max_tickets_per_batch,
        )

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
