from django.db import models

from labour.models import SignupExtraBase


SHIRT_SIZES = [
	(u'NO_SHIRT', u'Ei paitaa'),

	(u'XS', u'XS'),
	(u'S', u'S'),
	(u'M', u'M'),
	(u'L', u'L'),
	(u'XL', u'XL'),
	(u'XXL', u'XXL'),
	(u'3XL', u'3XL'),
	(u'4XL', u'4XL'),
	(u'5XL', u'5XL'),

	(u'LF_XS', u'XS Ladyfit'),
	(u'LF_S', u'S Ladyfit'),
	(u'LF_M', u'M Ladyfit'),
	(u'LF_L', u'L Ladyfit'),
	(u'LF_XL', u'XL Ladyfit'),
]


class SignupExtra(SignupExtraBase):
	shirt_size = models.CharField(max_length=8, choices=SHIRT_SIZES)

	@classmethod
	def init_form(cls, *args, **kwargs):
		from .forms import SignupExtraForm
		return SignupExtraForm(*args, **kwargs)