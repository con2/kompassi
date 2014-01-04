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


class SignupExtraBase(models.Model):
	signup = models.OneToOneField(Signup, related_name="+", primary_key=True)

	@classmethod
	def init_form(cls, *args, **kwargs):
		raise NotImplemented('Remember to override init_form in your SignupExtra model')

	class Meta:
		abstract = True


class Qualification(models.Model):
	name = models.CharField(max_length=31)
	qualification_extra_content_type = models.ForeignKey('contenttypes.ContentType', null=True, blank=True)

	@property
	def qualification_extra_model(self):
	    return self.qualification_extra_content_type.model_class() if self.qualification_extra_content_type else None

	@classmethod
	def create_dummy(cls):
		return cls.objects.create(
			name='Dummy qualification'
		)


class PersonQualification(models.Model):
	person = models.ForeignKey('core.Person')
	qualification = models.ForeignKey(Qualification)

	@property
	def qualification_extra(self):
		return self.qualification.qualification_extra_model.objects.get(personqualification=self)


class QualificationExtraBase(models.Model):
	personqualification = models.OneToOneField(PersonQualification, related_name="+", primary_key=True)

	@classmethod
	def init_form(cls, *args, **kwargs):
		raise NotImplemented('Remember to override init_form in your QualificationExtra model')

	class Meta:
		abstract = True