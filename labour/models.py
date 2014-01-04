from django.db import models


class EventMeta(models.Model):
	event = models.OneToOneField('core.Event', primary_key=True)
	signup_extra_content_type = models.ForeignKey('contenttypes.ContentType')

	@property
	def signup_extra_model(self):
	    return self.signup_extra_content_type.model_class()


class Signup(models.Model):
	person = models.ForeignKey('core.Person')
	event = models.ForeignKey('core.Event')

	@property
	def signup_extra(self):
		return self.event.signup_extra_model.objects.get(signup=self)	


class SignupExtra(models.Model):
	signup = models.OneToOneField(Signup, related_name="-")

	class Meta:
		abstract = True


