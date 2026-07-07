import logging
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

logger = logging.getLogger(__name__)

INVALID_SSN = "000000A0000"

# Finnish SSNs and Finnish PIA-protected identifiers — replace with clearly invalid placeholder.
FORM_DATA_SSN_SLUGS = frozenset(
    [
        "hetu",
        "henkilotunnus",
        "ssn",
        "social_security_number",
        "socialSecurityNumber",
        "personal_identification_number",
        "personalIdentificationNumber",
    ]
)

# Standard PII + GDPR Art. 9 special category health data — clear to empty string.
FORM_DATA_CLEAR_SLUGS = frozenset(
    [
        "first_name",
        "firstName",
        "last_name",
        "lastName",
        "official_first_names",
        "name",
        "email",
        "phone",
        "phone_number",
        "phoneNumber",
        "address",
        "discord",
        "discord_handle",
        "discordHandle",
        "nick",
        # Special diet / health data (GDPR Art. 9)
        "special_diet_other",
        "erityisruokavalio",
        "allergies",
        "dietary_restrictions",
        "dietaryRestrictions",
        "special_diets",
    ]
)


class Command(BaseCommand):
    help = (
        "Pseudonymize all personal data in the database. "
        "Intended to run against a temporary copy of the production database "
        "created by scripts/make-pseudonymized-dump.sh. "
        "The database name must contain 'pseudo'. "
        "Note: form_data PII scrubbing is best-effort based on known field slugs; "
        "custom slugs outside the known list will not be scrubbed."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            dest="yes",
            help="Confirm that you want to pseudonymize this database.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry_run",
            help="Print counts of affected records without writing anything.",
        )

    def handle(self, *args, **options):
        self._check_safety(options["yes"])

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING("DRY RUN — no changes will be written."))
            self._report_counts()
            return

        with transaction.atomic():
            self._pseudonymize_persons()
            self._pseudonymize_tickets_v2_orders()
            self._pseudonymize_forms_responses()
            self._pseudonymize_involvement_invitations()
            self._pseudonymize_signup_extras()
            self._pseudonymize_zombie_enrollment()
            self._pseudonymize_zombie_tickets_customers()
            self._pseudonymize_zombie_programme_feedback()
            self._delete_one_time_tokens()
            self._delete_smtp_passwords()
            self._delete_keypairs()
            self._delete_email_aliases()

        self.stdout.write(self.style.SUCCESS("Pseudonymization complete."))

    def _check_safety(self, yes: bool) -> None:
        if not yes:
            raise CommandError("Pass --yes to confirm you want to pseudonymize this database.")
        db_name = settings.DATABASES["default"]["NAME"]
        if "pseudo" not in db_name:
            raise CommandError(
                f"Database name {db_name!r} does not contain 'pseudo'. "
                "This command is intended to run against a temporary copy created by "
                "scripts/make-pseudonymized-dump.sh. "
                "If you set up the temp database manually, rename it to include 'pseudo'."
            )

    def _pseudonymize_persons(self) -> None:
        from kompassi.core.models import Person

        User = get_user_model()
        count = 0

        for person in Person.objects.select_related("user").iterator(chunk_size=500):
            pk = person.pk
            person.first_name = f"Person{pk}"
            person.official_first_names = f"Person{pk}"
            person.surname = "Testinen"
            person.nick = f"person{pk}" if person.nick else ""
            person.discord_handle = f"person{pk}" if person.discord_handle else ""
            person.email = f"person{pk}@example.com"
            person.phone = f"+358000{pk:06d}"
            person.muncipality = "Testilä"
            person.notes = ""
            if person.birth_date:
                person.birth_date = date(person.birth_date.year, 1, 1)
            # person.save() syncs first_name/surname/email to person.user
            person.save()
            if person.user_id:
                person.user.set_unusable_password()
                person.user.save(update_fields=["password"])
            count += 1

        orphan_count = User.objects.filter(person__isnull=True).update(first_name="", last_name="", email="")
        for user in User.objects.filter(person__isnull=True).iterator(chunk_size=500):
            user.set_unusable_password()
            user.save(update_fields=["password"])

        self.stdout.write(f"  Persons: {count}, orphan users: {orphan_count}")

    def _pseudonymize_tickets_v2_orders(self) -> None:
        from kompassi.tickets_v2.models.order import Order
        from kompassi.tickets_v2.models.receipt import Receipt

        Order.objects.update(first_name="Order", last_name="Testinen", phone="")
        for order in Order.objects.only("id", "order_number").iterator(chunk_size=1000):
            Order.objects.filter(id=order.id).update(email=f"order{order.order_number}@example.com")

        receipt_count = Receipt.objects.update(email="")
        self.stdout.write(f"  Orders: {Order.objects.count()}, receipts cleared: {receipt_count}")

    def _pseudonymize_forms_responses(self) -> None:
        from kompassi.forms.models.response import Response

        Response.objects.update(ip_address="127.0.0.1", cached_key_fields={})

        count = 0
        scrubbed = 0
        for response in Response.objects.only("id", "form_data").iterator(chunk_size=500):
            new_data = dict(response.form_data)
            changed = False
            for slug in FORM_DATA_SSN_SLUGS:
                if slug in new_data:
                    new_data[slug] = INVALID_SSN
                    changed = True
            for slug in FORM_DATA_CLEAR_SLUGS:
                if slug in new_data:
                    new_data[slug] = ""
                    changed = True
            if changed:
                response.form_data = new_data
                response.save(update_fields=["form_data"])
                scrubbed += 1
            count += 1

        self.stdout.write(f"  Responses: {count} processed, {scrubbed} form_data scrubbed")

    def _pseudonymize_involvement_invitations(self) -> None:
        from kompassi.involvement.models.invitation import Invitation

        count = 0
        for invitation in Invitation.objects.only("id").iterator(chunk_size=500):
            Invitation.objects.filter(id=invitation.id).update(email=f"invitation-{str(invitation.id)[:8]}@example.com")
            count += 1

        self.stdout.write(f"  Invitations: {count}")

    def _pseudonymize_signup_extras(self) -> None:
        from django.apps import apps

        from kompassi.labour.models.signup_extras import SignupExtraMixin

        for model in apps.get_models():
            if not (isinstance(model, type) and issubclass(model, SignupExtraMixin)):
                continue
            if model.get_special_diet_field():
                for instance in model.objects.iterator(chunk_size=500):
                    instance.special_diet.clear()  # type: ignore[attr-defined]
                self.stdout.write(f"  {model.__name__} special_diet cleared")
            if model.get_special_diet_other_field():
                count = model.objects.update(special_diet_other="")
                self.stdout.write(f"  {model.__name__} special_diet_other cleared: {count}")

    def _pseudonymize_zombie_enrollment(self) -> None:
        from kompassi.zombies.enrollment.models.enrollment import Enrollment

        count = Enrollment.objects.update(
            personal_identification_number=INVALID_SSN,
            address="",
            zip_code="",
            city="",
        )
        for enrollment in Enrollment.objects.iterator(chunk_size=500):
            enrollment.special_diet.clear()

        self.stdout.write(f"  Zombie enrollments: {count}")

    def _pseudonymize_zombie_tickets_customers(self) -> None:
        from kompassi.zombies.tickets.models.LEGACY_TICKETSV1_customer import Customer

        count = 0
        for customer in Customer.objects.only("pk").iterator(chunk_size=500):
            Customer.objects.filter(pk=customer.pk).update(
                first_name="Customer",
                last_name="Testinen",
                email=f"customer{customer.pk}@example.com",
                phone_number="",
            )
            count += 1

        self.stdout.write(f"  Legacy customers: {count}")

    def _pseudonymize_zombie_programme_feedback(self) -> None:
        from kompassi.zombies.programme.models.programme_feedback import ProgrammeFeedback

        count = ProgrammeFeedback.objects.update(ip_address="127.0.0.1", author_external_username="")
        self.stdout.write(f"  Programme feedback: {count}")

    def _delete_one_time_tokens(self) -> None:
        from kompassi.core.models.email_verification_token import EmailVerificationToken
        from kompassi.core.models.password_reset_token import PasswordResetToken
        from kompassi.tickets_v2.models.order_cancellation_token import OrderCancellationToken

        n1, _ = EmailVerificationToken.objects.all().delete()
        n2, _ = PasswordResetToken.objects.all().delete()
        n3, _ = OrderCancellationToken.objects.all().delete()
        self.stdout.write(f"  Deleted tokens: {n1} email verification, {n2} password reset, {n3} order cancellation")

    def _delete_smtp_passwords(self) -> None:
        from kompassi.access.models.smtp_password import SMTPPassword

        count, _ = SMTPPassword.objects.all().delete()
        self.stdout.write(f"  Deleted SMTP passwords: {count}")

    def _delete_keypairs(self) -> None:
        from kompassi.forms.models.keypair import KeyPair

        count, _ = KeyPair.objects.all().delete()
        self.stdout.write(f"  Deleted keypairs: {count}")

    def _delete_email_aliases(self) -> None:
        from kompassi.access.models.email_alias import EmailAlias

        count, _ = EmailAlias.objects.all().delete()
        self.stdout.write(f"  Deleted email aliases: {count}")

    def _report_counts(self) -> None:
        from kompassi.access.models.email_alias import EmailAlias
        from kompassi.access.models.smtp_password import SMTPPassword
        from kompassi.core.models import Person
        from kompassi.core.models.email_verification_token import EmailVerificationToken
        from kompassi.core.models.password_reset_token import PasswordResetToken
        from kompassi.forms.models.keypair import KeyPair
        from kompassi.forms.models.response import Response
        from kompassi.involvement.models.invitation import Invitation
        from kompassi.tickets_v2.models.order import Order
        from kompassi.tickets_v2.models.order_cancellation_token import OrderCancellationToken
        from kompassi.zombies.enrollment.models.enrollment import Enrollment
        from kompassi.zombies.tickets.models.LEGACY_TICKETSV1_customer import Customer

        self.stdout.write(f"  Persons: {Person.objects.count()}")
        self.stdout.write(f"  Orders: {Order.objects.count()}")
        self.stdout.write(f"  Responses: {Response.objects.count()}")
        self.stdout.write(f"  Invitations: {Invitation.objects.count()}")
        self.stdout.write(f"  Zombie enrollments: {Enrollment.objects.count()}")
        self.stdout.write(f"  Legacy customers: {Customer.objects.count()}")
        self.stdout.write(f"  Email verification tokens: {EmailVerificationToken.objects.count()}")
        self.stdout.write(f"  Password reset tokens: {PasswordResetToken.objects.count()}")
        self.stdout.write(f"  Order cancellation tokens: {OrderCancellationToken.objects.count()}")
        self.stdout.write(f"  SMTP passwords: {SMTPPassword.objects.count()}")
        self.stdout.write(f"  Keypairs: {KeyPair.objects.count()}")
        self.stdout.write(f"  Email aliases: {EmailAlias.objects.count()}")
