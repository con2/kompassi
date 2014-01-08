# encoding: utf-8

from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div

def indented_without_label(input):
    return Div(
              Div(
                Submit('submit', u'Kirjaudu sisään', css_class='btn-primary'),
                css_class='controls col-md-2 col-md-offset-2'
              ),
              css_class='form-group'
            )

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            'username',
            'password',
            indented_without_label(Submit('submit', u'Kirjaudu sisään', css_class='btn-primary'))
        )