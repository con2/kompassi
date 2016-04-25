# encoding: utf-8

from datetime import date

from django.conf import settings
from django.utils.dateformat import format as format_date
from django.utils.translation import ugettext_lazy as _


EMAIL_LENGTH = PHONE_NUMBER_LENGTH = 255

# TODO how do I localize this
BIRTH_DATE_HELP_TEXT = u'Syntymäaika muodossa {0}'.format(
    format_date(date(1994, 2, 24), settings.DATE_FORMAT)
)

NAME_DISPLAY_STYLE_CHOICES = [
    (u'firstname_nick_surname', _(u'Firstname "Nickname" Surname')),
    (u'firstname_surname', _(u'Firstname Surname')),
    (u'firstname', _(u'Firstname')),
    (u'nick', _(u'Nickname')),
]

NAME_DISPLAY_STYLE_FORMATS = dict(
    firstname=u'{self.first_name}',
    firstname_nick_surname=u'{self.first_name} "{self.nick}" {self.surname}',
    firstname_surname=u'{self.first_name} {self.surname}',
    nick=u'{self.nick}',
)