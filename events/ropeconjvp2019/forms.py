from django import forms

from core.utils import horizontal_form_helper
from enrollment.models import Enrollment


class EnrollmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()

        for field_name in (
            'personal_identification_number',
            'address',
            'zip_code',
            'city',
            'traconjv_avow_and_affirm',
            'traconjv_solemnly_swear',
        ):
            self.fields[field_name].required = True

        self.fields['traconjv_avow_and_affirm'].label = 'Vakuutan olevani lain tarkoittamalla tavalla rehellinen ja luotettava ja henkilökohtaisilta ominaisuuksiltani tehtävään sopiva, eikä minulla ole voimassaolevia tai vanhoja tuomioita tai rikosrekisteriä.'
        self.fields['traconjv_solemnly_swear'].label = 'Vakuutan antamani tiedot oikeiksi. Ilmoittautumalla sitoudun osallistumaan peruskurssille 25.–31.3. pääkaupunkiseudulla ja järjestyksenvalvojana Ropecon 2019- ja Ropecon 2020 -tapahtumiin.'

    class Meta:
        model = Enrollment
        fields = (
            'personal_identification_number',
            'address',
            'zip_code',
            'city',
            'traconjv_avow_and_affirm',
            'traconjv_solemnly_swear',
        )
