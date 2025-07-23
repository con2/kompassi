from crispy_forms.helper import FormHelper
from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from kompassi.core.utils import initialize_form


class CreateBatchForm(forms.Form):
    max_items = forms.IntegerField(label="Kuinka monta tilausta (enintään)?", initial=500, min_value=1, max_value=10000)

    def __init__(self, *args, **kwargs):
        kwargs.pop("event")

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class HiddenBatchCrouchingForm(forms.Form):
    batch_id = forms.IntegerField(required=True)


def batches_view(Batch, template, CreateBatchForm=CreateBatchForm, created_at_field="created_at"):
    """
    Creates a view the like of which you see in two places - tickets admin and badges admin.
    It is used to manage batches of things that in turn are handled together.

    In tickets, this is used for printing and mailing orders.

    In badges, this is used for printing badges.

    You need to wrap it in a standard app_admin_required decorator of your own (hence the vars).
    """

    def _badges_view(request, vars, event):
        new_batch_form = initialize_form(CreateBatchForm, request, event=event)

        if request.method == "POST":
            if "new-batch" in request.POST:
                if new_batch_form.is_valid():
                    batch = Batch.create(event=event, **new_batch_form.cleaned_data)
                    messages.success(request, f"Erä {batch.pk} on luotu onnistuneesti")
                    return redirect(request.path)
                else:
                    messages.error(request, "Ole hyvä ja korjaa lomakkeen virheet.")

            elif "cancel-batch" in request.POST or "confirm-batch" in request.POST:
                hidden_batch_crouching_form = HiddenBatchCrouchingForm(request.POST)

                if hidden_batch_crouching_form.is_valid():
                    batch = get_object_or_404(
                        Batch, event=event, pk=hidden_batch_crouching_form.cleaned_data["batch_id"]
                    )

                    if "cancel-batch" in request.POST and batch.can_cancel:
                        batch.cancel()
                        messages.success(request, "Erä peruttiin.")
                        return redirect(request.path)

                    elif "confirm-batch" in request.POST and batch.can_confirm:
                        batch.confirm()
                        messages.success(request, "Erä on merkitty valmiiksi.")
                        return redirect(request.path)

                # error
                messages.error(request, "Et ole tulitikku kung-fulleni.")

        vars.update(new_batch_form=new_batch_form, batches=Batch.objects.filter(event=event).order_by(created_at_field))

        return render(request, template, vars)

    return _badges_view
