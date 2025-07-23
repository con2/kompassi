from functools import cached_property

from django.db import models


class SignupExtraMixin:
    @classmethod
    def get_form_class(cls):
        raise NotImplementedError("Remember to implement form_class in your SignupExtra class")

    @classmethod
    def get_programme_form_class(cls):
        return cls.get_form_class()

    @classmethod
    def get_shirt_size_field(cls):
        return cls.get_field("shirt_size", None)

    @classmethod
    def get_shirt_type_field(cls):
        return cls.get_field("shirt_type", None)

    @classmethod
    def get_special_diet_field(cls):
        return cls.get_m2m_field("special_diet", None)

    @classmethod
    def get_special_diet_model(cls):
        special_diet_field = cls.get_special_diet_field()
        return special_diet_field.related_model if special_diet_field else None

    @property
    def formatted_special_diet(self):
        if not self.__class__.get_special_diet_field():
            return ""

        return ", ".join(sd.name for sd in self.special_diet.all())

    @classmethod
    def get_special_diet_other_field(cls):
        return cls.get_field("special_diet_other", None)

    @classmethod
    def get_field(cls, field_name, default=None):
        if not hasattr(cls, "_fields_by_name"):
            cls._fields_by_name = {field.name: field for field in cls._meta.fields}

        return cls._fields_by_name.get(field_name, default)

    @classmethod
    def get_m2m_field(cls, field_name, default=None):
        if not hasattr(cls, "_m2m_fields_by_name"):
            cls._m2m_fields_by_name = {field.name: field for field in cls._meta.many_to_many}

        return cls._m2m_fields_by_name.get(field_name, default)

    def apply_state(self):
        self.is_active = self.determine_is_active()
        self.save()

    def __str__(self):
        return self.signup.__str__() if self.signup else "None"


class SignupExtraBase(SignupExtraMixin, models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="%(app_label)s_signup_extras")
    person = models.OneToOneField("core.Person", on_delete=models.CASCADE, related_name="%(app_label)s_signup_extra")

    is_active = models.BooleanField(default=True)

    supports_programme = True
    schema_version = 2

    def determine_is_active(self):
        # See if this SignupExtra is active due to participation in volunteer work
        if self.signup and self.signup.is_active:
            return True

        # See if this SignupExtra is active due to programme roles
        from kompassi.zombies.programme.models.programme import PROGRAMME_STATES_ACTIVE
        from kompassi.zombies.programme.models.programme_role import ProgrammeRole

        return ProgrammeRole.objects.filter(
            programme__category__event=self.event,
            programme__state__in=PROGRAMME_STATES_ACTIVE,
            person=self.person,
        ).exists()

    @cached_property
    def discord_roles(self):
        result = []

        if self.signup and self.signup.is_alive:
            result.extend(pc.name for pc in self.signup.personnel_classes.all())

        from kompassi.zombies.programme.models.programme import PROGRAMME_STATES_LIVE
        from kompassi.zombies.programme.models.programme_role import ProgrammeRole

        programme_roles = ProgrammeRole.objects.filter(
            programme__category__event=self.event,
            programme__state__in=PROGRAMME_STATES_LIVE,
            person=self.person,
        ).select_related("role")

        result.extend(pr.role.public_title for pr in programme_roles)

        return result

    # NOTE: changing this to cached_property will break a test. beware
    @property
    def signup(self):
        from .signup import Signup

        try:
            return Signup.objects.get(event=self.event, person=self.person)
        except Signup.DoesNotExist:
            return None

    @classmethod
    def get_for_event_and_person(cls, event, person):
        return cls.objects.get(event=event, person=person)

    @classmethod
    def for_event_and_person(cls, event, person):
        try:
            return cls.objects.get(event=event, person=person)
        except cls.DoesNotExist:
            return cls(event=event, person=person)

    @classmethod
    def for_signup(cls, signup):
        try:
            return cls.get_for_event_and_person(signup.event, signup.person)
        except cls.DoesNotExist:
            return cls(event=signup.event, person=signup.person)

    class Meta:
        abstract = True


class EmptySignupExtra(SignupExtraBase):
    supports_programme = False

    @classmethod
    def get_form_class(cls):
        from ..forms import EmptySignupExtraForm

        return EmptySignupExtraForm


class ObsoleteSignupExtraBaseV1(SignupExtraMixin, models.Model):
    """
    Because `signup` is the primary key, we choose to retain this abstract base model and make a new one
    that refers to `event` and `person` instead.
    """

    signup = models.OneToOneField(
        "labour.Signup", on_delete=models.CASCADE, related_name="%(app_label)s_signup_extra", primary_key=True
    )
    is_active = models.BooleanField(default=True)

    supports_programme = False
    schema_version = 1

    def determine_is_active(self):
        return self.signup.is_active

    @property
    def event(self):
        return self.signup.event if self.signup is not None else None

    @property
    def person(self):
        return self.signup.person if self.signup is not None else None

    @classmethod
    def get_for_event_and_person(cls, event, person):
        return cls.objects.get(signup__event=event, signup__person=person)

    @classmethod
    def for_signup(cls, signup):
        try:
            return cls.objects.get(signup=signup)
        except cls.DoesNotExist:
            return cls(signup=signup)

    class Meta:
        abstract = True


class ObsoleteEmptySignupExtraV1(ObsoleteSignupExtraBaseV1):
    @classmethod
    def get_form_class(cls):
        raise NotImplementedError("ObsoleteEmptySignupExtraV1Form")
