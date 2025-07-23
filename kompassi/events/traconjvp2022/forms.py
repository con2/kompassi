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
            "traconjv_avow_and_affirm",
            "traconjv_solemnly_swear",
        ):
            self.fields[field_name].required = True

        self.fields[
            "traconjv_avow_and_affirm"
        ].label = "Ilmoittautumalla sitoudun osallistumaan peruskurssin kaikille oppitunneille pe 5.8.,  la 6.8., su 7.8., pe 12.8., la 13.8. ja su 21.8.. Tampereella ja toimimaan järjestyksenvalvojana kahdessa seuraavassa Tracon-tapahtumassa. Ymmärrän, että saatan joutua maksamaan kurssista Tracon ry:lle koituvat kulut takaisin, jos en suorita kurssia hyväksytysti tai en voi toimia sovitusti järjestyksenvalvojana tapahtumissa."

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
            "traconjv_avow_and_affirm",
            "traconjv_solemnly_swear",
        )
