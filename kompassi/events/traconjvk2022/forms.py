from django import forms

from kompassi.core.utils import horizontal_form_helper
from kompassi.zombies.enrollment.models import Enrollment


class EnrollmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()

        for field_name in (
            "personal_identification_number",
            "address",
            "zip_code",
            "city",
            "traconjv_expiring",
            "traconjv_when",
            "traconjv_avow_and_affirm",
            "traconjv_solemnly_swear",
        ):
            self.fields[field_name].required = True

        self.fields[
            "traconjv_avow_and_affirm"
        ].label = "Ilmoittautumalla sitoudun osallistumaan kertauskurssille su 14.8. Tampereella ja toimimaan järjestyksenvalvojana Tracon 2022-tapahtumassa 5. - 7.9.2022. Ymmärrän, että saatan joutua maksamaan kurssista Tracon ry:lle koituvat kulut takaisin, jos en suorita kurssia hyväksytysti tai en voi toimia sovitusti järjestyksenvalvojana tapahtumissa."

        self.fields[
            "traconjv_solemnly_swear"
        ].label = "Vakuutan antamani tiedot oikeiksi sekä olevani lain tarkoittamalla tavalla rehellinen ja luotettava ja henkilökohtaisilta ominaisuuksiltani tehtävään sopiva, eikä minulla ole voimassaolevia tai vanhoja tuomioita tai rikosrekisteriä."

    class Meta:
        model = Enrollment
        fields = (
            "personal_identification_number",
            "address",
            "zip_code",
            "city",
            "traconjv_expiring",
            "traconjv_when",
            "traconjv_avow_and_affirm",
            "traconjv_solemnly_swear",
        )
