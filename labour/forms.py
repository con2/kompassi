# encoding: utf-8

from datetime import date, datetime

from django import forms
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import Layout, Fieldset

from core.forms import PersonForm
from core.models import Person
from core.utils import horizontal_form_helper, indented_without_label, slugify

from .models import (
    AlternativeFormMixin,
    Signup,
    JobCategory,
    EmptySignupExtra,
    LabourEventMeta,
    PersonnelClass,
    WorkPeriod,
)


# http://stackoverflow.com/a/9754466
def calculate_age(born, today):
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class AdminPersonForm(PersonForm):
    age_now = forms.IntegerField(required=False, label=u'Ikä nyt')
    age_event_start = forms.IntegerField(required=False, label=u'Ikä tapahtuman alkaessa')

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        super(AdminPersonForm, self).__init__(*args, **kwargs)

        self.fields['age_now'].widget.attrs['readonly'] = True
        self.fields['age_event_start'].widget.attrs['readonly'] = True
        if self.instance.birth_date is not None:
            self.fields['age_now'].initial = calculate_age(self.instance.birth_date, date.today())
            if event.start_time is not None:
                self.fields['age_event_start'].initial = calculate_age(self.instance.birth_date, event.start_time.date())

        # XXX copypasta
        self.helper.layout = Layout(
            'first_name',
            'surname',
            'nick',
            'preferred_name_display_style',
            'birth_date',
            'age_now', # not in PersonForm
            'age_event_start', # not in PersonForm
            'phone',
            'email',
            'may_send_info',
        )

    class Meta:
        model = Person
        fields = (
            'first_name',
            'surname',
            'nick',
            'preferred_name_display_style',
            'birth_date',
            'age_now', # not in PersonForm
            'age_event_start', # not in PersonForm
            'phone',
            'email',
            'may_send_info',
        )


class SignupFormMixin(object):
    def get_job_categories_query(self, event, admin=False):
        q = Q(event=event, personnel_classes__app_label='labour')

        if not admin:
            # For non-admin usage, restrict to public JCs only.
            q = q & Q(public=True)

            if self.instance.pk is not None:
                # Also include those the user is signed up to whether or not they are public.
                q = q | Q(signup_set=self.instance)

        return q

    def get_job_categories(self, event, admin=False):
        from .models import JobCategory
        job_categories_query = self.get_job_categories_query(event, admin)
        return JobCategory.objects.filter(job_categories_query).distinct().order_by('id')


class SignupForm(forms.ModelForm, SignupFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        admin = kwargs.pop('admin')

        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['job_categories'].queryset = self.get_job_categories(event, admin)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Tehtävät',
                'job_categories'
            ),
        )

    def clean_job_categories(self):
        job_categories = self.cleaned_data['job_categories']

        if not all(jc.is_person_qualified(self.instance.person) for jc in job_categories):
            raise forms.ValidationError(u'Sinulla ei ole vaadittuja pätevyyksiä valitsemiisi tehtäviin.')

        return job_categories

    class Meta:
        model = Signup
        fields = ('job_categories',)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )


class EmptySignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = EmptySignupExtra
        exclude = ('signup',)


class SignupAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(SignupAdminForm, self).__init__(*args, **kwargs)

        self.fields['job_categories_accepted'].queryset = JobCategory.objects.filter(event=event)
        self.fields['job_categories_rejected'].queryset = self.fields['job_categories_accepted'].queryset
        self.fields['personnel_classes'].queryset = PersonnelClass.objects.filter(event=event).order_by('priority')

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Signup
        fields = (
            'job_title',
            'personnel_classes',
            'job_categories_accepted',
            'job_categories_rejected',
            'xxx_interim_shifts',
            'notes',
        )
        widgets = dict(
            personnel_classes=forms.CheckboxSelectMultiple,
            job_categories_accepted=forms.CheckboxSelectMultiple,
            job_categories_rejected=forms.CheckboxSelectMultiple,
        )

    def clean_job_categories_accepted(self):
        job_categories_accepted = self.cleaned_data['job_categories_accepted']

        if self.instance.is_accepted and not job_categories_accepted and self.instance.job_categories.count() != 1:
            raise forms.ValidationError(u'Kun ilmoittautuminen on hyväksytty, tulee valita vähintään yksi tehtäväalue. Henkilön hakema tehtävä ei ole yksikäsitteinen, joten tehtäväaluetta ei voitu valita automaattisesti.')
        elif (self.instance.is_rejected or self.instance.is_cancelled) and job_categories_accepted:
            raise forms.ValidationError(u'Kun ilmoittautuminen on hylätty, mikään tehtäväalue ei saa olla valittuna.')

        return job_categories_accepted

    def clean_personnel_classes(self):
        personnel_classes = self.cleaned_data['personnel_classes']

        if self.instance.is_accepted and not personnel_classes:
            raise forms.ValidationError(u'Kun ilmoittautuminen on hyväksytty, tulee valita vähintään yksi Henkilöstöluokka.')
        elif (self.instance.is_rejected or self.instance.is_cancelled) and personnel_classes:
            raise forms.ValidationError(u'Kun ilmoittautuminen on hylätty, mikään Henkilöstöluokka ei saa olla valittuna.')

        return personnel_classes


class RemoveJobCategoryForm(forms.Form):
    remove = forms.IntegerField(required=True)


class JobCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(JobCategoryForm, self).__init__(*args, **kwargs)

        self.fields['personnel_classes'].queryset = PersonnelClass.objects.filter(event=event).order_by('priority')
        self.fields['personnel_classes'].required = True

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = JobCategory
        fields = (
            'name',
            'description',
            'public',
            'required_qualifications',
            'personnel_classes',
        )
        widgets = dict(
            required_qualifications=forms.CheckboxSelectMultiple,
            personnel_classes=forms.CheckboxSelectMultiple,
        )

    def clean_name(self):
        name = self.cleaned_data['name']

        if name and not self.instance.pk:
            slug = slugify(name)
            if JobCategory.objects.filter(event=self.instance.event, slug=slug).exists():
                raise forms.ValidationError(_('The slug that would be derived from this name is already taken. Please choose another name.'))

        return name


class StartStopForm(forms.ModelForm):
    # XXX get a date picker
    registration_opens = forms.DateTimeField(
        required=False,
        label=_("Registration opens"),
    )
    registration_closes = forms.DateTimeField(
        required=False,
        label=_("Registration closes"),
        help_text=_("Format: YYYY-MM-DD HH:MM:SS"),
    )

    def __init__(self, *args, **kwargs):
        super(StartStopForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    def clean_registration_closes(self):
        registration_opens = self.cleaned_data.get('registration_opens')
        registration_closes = self.cleaned_data.get('registration_closes')

        if registration_opens and registration_closes and registration_opens >= registration_closes:
            raise forms.ValidationError(_("The registration closing time must be after the registration opening time."))

        return registration_closes

    class Meta:
        model = LabourEventMeta
        fields = (
            'registration_opens',
            'registration_closes',
        )