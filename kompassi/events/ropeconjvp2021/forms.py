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
        ].label = """Lain mukaan järjestyksenvalvojaksi voidaan hyväksyä se, joka:<br>
1) on täyttänyt 18 vuotta;<br>
2) tunnetaan rehelliseksi ja luotettavaksi ja on henkilökohtaisilta ominaisuuksiltaan tehtävään sopiva.<br><br>

Näiden ehtojen lisäksi järjestyksenvalvojakortin myöntäminen edellyttää todistusta tämän perus- tai kertauskurssin hyväksytystä suorituksesta.<br><br>

Vakuutan täyttäväni järjestyksenvalvojaksi hyväksymiselle määritellyt ehdot, ja osallistuvani kurssin kaikille tunneille."""
        self.fields[
            "traconjv_solemnly_swear"
        ].label = "Vakuutan antamani tiedot oikeiksi. Ilmoittautumalla sitoudun osallistumaan peruskurssille ilmoitettuna päivinä pääkaupunkiseudulla ja järjestyksenvalvojana seuraavaan kahteen Ropecon-tapahtumaan."

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
