from django.utils.translation import gettext_lazy as _

EMAIL_LENGTH = PHONE_NUMBER_LENGTH = 255

BIRTH_DATE_HELP_TEXT = _("Birth date in the following format: DD.MM.YYYY")

NAME_DISPLAY_STYLE_CHOICES = [
    ("firstname_nick_surname", _('Firstname "Nickname" Surname')),
    ("firstname_surname", _("Firstname Surname")),
    ("firstname", _("Firstname")),
    ("nick", _("Nickname")),
]

NAME_DISPLAY_STYLE_FORMATS = dict(
    firstname="{self.first_name}",
    firstname_nick_surname='{self.first_name} "{self.nick}" {self.surname}',
    firstname_surname="{self.first_name} {self.surname}",
    nick="{self.nick}",
)
