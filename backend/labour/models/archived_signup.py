from django.db import models

from event_log_v2.utils.emit import emit

from .constants import JOB_TITLE_LENGTH
from .signup import SignupMixin

# Only make positive archive records.
ARCHIVE_STATES = [
    "accepted",
    "confirmation",
    "finished",
    "arrived",
    "honr_discharged",
]


class ArchivedSignup(SignupMixin, models.Model):
    """
    Ducks just enough of the Signup class to represent archived signups in certain places.
    """

    person = models.ForeignKey("core.Person", on_delete=models.CASCADE, related_name="archived_signups")
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="archived_signups")

    personnel_classes = models.ManyToManyField(
        "labour.PersonnelClass",
        blank=True,
        verbose_name="Henkilöstöluokat",
        related_name="archived_signups",
    )
    job_categories_accepted = models.ManyToManyField(
        "labour.JobCategory",
        blank=True,
        related_name="archived_signups",
        verbose_name="Hyväksytyt tehtäväalueet",
    )

    job_title = models.CharField(
        max_length=JOB_TITLE_LENGTH,
        blank=True,
        default="",
        verbose_name="Tehtävänimike",
    )

    state = "archived"
    is_accepted = True

    def __str__(self):
        p = self.person.full_name if self.person else "None"
        e = self.event.name if self.event else "None"

        return f"{p} / {e} (ARCHIVED)"

    @property
    def some_job_title(self):
        return self.job_title

    @classmethod
    def archive_signup(cls, signup):
        """
        If the signup is in a positive final state, archives it. Otherwise deletes it.
        An event log entry is emitted in both cases.

        Archiving a signup means making an ArchivedSignup of it and deleting the original
        Signup and its SignupExtra.
        """
        person = signup.person
        event = signup.event

        if signup.state in ARCHIVE_STATES:
            event_type = "labour.signup.archived"

            archived_signup, created = ArchivedSignup.objects.get_or_create(
                person=signup.person,
                event=signup.event,
                job_title=signup.some_job_title,
            )

            archived_signup.job_categories_accepted.set(signup.job_categories_accepted.all())
            archived_signup.personnel_classes.set(signup.personnel_classes.all())
        else:
            event_type = "labour.signup.deleted"

        emit(
            event_type,
            event=event.slug,
            organization=event.organization.slug,
            person=person.pk,
        )
