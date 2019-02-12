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
        self.fields['traconjv_solemnly_swear'].label = 'Vakuutan antamani tiedot oikeiksi. Ilmoittautumalla sitoudun osallistumaan peruskurssille 30.-31.3., 6.-7.4. ja 13.4. Tampereella ja järjestyksenvalvojana Tracon 2019 ja Tracon 2020-tapahtumissa.'

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

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            concon_parts=forms.CheckboxSelectMultiple,
        )
