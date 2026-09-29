"""
Turns a copy of the production database into one that can be handed to developers.

Every field that `is_suspicious` flags must be covered by a rule in `RULES` or listed in
`NOT_PERSONAL`. `core/tests.py` fails otherwise, so a new model or field holding personal data
cannot slip past the pseudonymizer unnoticed. `manage.py pseudonymize_db --check` prints the
fields that still need a decision.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from django.apps import apps
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import connection, models
from django.db.models import Case, CharField, OuterRef, Subquery, Value, When
from django.db.models.expressions import Combinable
from django.db.models.functions import Cast, Coalesce, Concat, LPad, TruncYear

from kompassi.core.models import Person
from kompassi.forms.models.field import FieldType
from kompassi.labour.models.signup_extras import SignupExtraMixin

REDACTED = "(pseudonymized)"
UNUSABLE_PASSWORD = f"{UNUSABLE_PASSWORD_PREFIX}pseudonymized"

ALL_FIELDS = frozenset({"*"})


@dataclass(frozen=True)
class Rule:
    model_label: str
    fields: frozenset[str]
    """Fields this rule makes safe to hand out. `ALL_FIELDS` means the rule deletes every row."""

    apply: Callable[[type[models.Model]], str]
    """Performs the rule on the model and returns a summary for the operator."""

    @property
    def model(self) -> type[models.Model]:
        return apps.get_model(self.model_label)


def delete_all(model_label: str) -> Rule:
    def apply(model: type[models.Model]) -> str:
        count, _ = model.objects.all().delete()
        return f"deleted {count}"

    return Rule(model_label, ALL_FIELDS, apply)


def update(model_label: str, **values: Any) -> Rule:
    def apply(model: type[models.Model]) -> str:
        return f"updated {model.objects.update(**values)}"

    return Rule(model_label, frozenset(values), apply)


def numbered(prefix: str, suffix: str = "", field: str = "pk") -> Combinable:
    return Concat(Value(prefix), Cast(field, output_field=CharField()), Value(suffix))


def unless_blank(field: str, expression: Combinable) -> Combinable:
    return Case(When(**{field: ""}, then=Value("")), default=expression)


def person_of(foreign_key: str, field: str) -> Subquery:
    return Subquery(Person.objects.filter(pk=OuterRef(foreign_key)).values(field)[:1])


def user_person(field: str) -> Subquery:
    return Subquery(Person.objects.filter(user=OuterRef("pk")).values(field)[:1])


def remove_json_keys(model_label: str, field: str, keys: list[str]) -> Rule:
    def apply(model: type[models.Model]) -> str:
        table = connection.ops.quote_name(model._meta.db_table)
        column = connection.ops.quote_name(model._meta.get_field(field).column)
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {table} SET {column} = {column} - %s::text[] WHERE {column} ?| %s::text[]",
                [keys, keys],
            )
            return f"removed {', '.join(keys)} from {cursor.rowcount}"

    return Rule(model_label, frozenset({field}), apply)


def is_free_text(field: models.Field) -> bool:
    return isinstance(field, (models.CharField, models.TextField)) and not field.choices and not field.primary_key


def signup_extra_rule(model: type[models.Model]) -> Rule:
    free_text_fields = [field.name for field in model._meta.concrete_fields if is_free_text(field)]

    def apply(model: type[models.Model]) -> str:
        count = model.objects.update(**{name: Value("") for name in free_text_fields})
        summary = f"cleared {', '.join(free_text_fields) or 'nothing'} on {count}"
        if special_diet_field := model.get_special_diet_field():  # type: ignore[attr-defined]
            deleted, _ = special_diet_field.remote_field.through.objects.all().delete()
            summary += f", {deleted} special diets"
        return summary

    return Rule(model._meta.label, frozenset(free_text_fields), apply)


def signup_extra_models() -> Iterable[type[models.Model]]:
    for model in apps.get_models():
        if issubclass(model, SignupExtraMixin):
            yield model


# Values that are a choice among options the organizers defined, not something the respondent wrote.
KEPT_FORM_FIELD_TYPES = frozenset(
    {
        FieldType.SINGLE_CHECKBOX,
        FieldType.TRISTATE,
        FieldType.SINGLE_SELECT,
        FieldType.MULTI_SELECT,
        FieldType.RADIO_MATRIX,
        FieldType.DIMENSION_SINGLE_SELECT,
        FieldType.DIMENSION_MULTI_SELECT,
        FieldType.DIMENSION_SINGLE_CHECKBOX,
        FieldType.NUMBER_FIELD,
        FieldType.DECIMAL_FIELD,
        FieldType.TIME_FIELD,
        FieldType.DATE_TIME_FIELD,
    }
)
REDACTED_FORM_FIELD_TYPES = frozenset(
    {
        FieldType.SINGLE_LINE_TEXT,
        FieldType.MULTI_LINE_TEXT,
        FieldType.MARKDOWN_TEXT,
    }
)


def pseudonymize_form_data(fields: list[dict[str, Any]], form_data: dict[str, Any]) -> dict[str, Any]:
    """
    Keeps answers that are choices, replaces free text with `REDACTED` and drops everything else,
    including date fields (birth dates), file uploads and answers to fields no longer on the form.
    Encrypted answers are dropped whatever the field type.
    """
    result = {}
    for field in fields:
        slug = field.get("slug")
        type = field.get("type")
        if not slug or field.get("encryptTo"):
            continue

        for key, value in form_data.items():
            if key != slug and not key.startswith(f"{slug}."):
                continue
            if type in KEPT_FORM_FIELD_TYPES:
                result[key] = value
            elif type in REDACTED_FORM_FIELD_TYPES:
                result[key] = REDACTED if value else value

    return result


def pseudonymize_responses(model: type[models.Model]) -> str:
    from kompassi.forms.models.form import Form
    from kompassi.forms.models.response import Response

    count = 0
    for form in Form.objects.select_related("survey").only("id", "cached_enriched_fields", "survey").iterator():
        responses = []
        for response in Response.objects.filter(form=form).only("id", "form", "form_data"):
            response.form = form
            response.form_data = pseudonymize_form_data(form.cached_enriched_fields, response.form_data)
            response.cached_key_fields = response._build_cached_key_fields(form.validated_fields)
            response.ip_address = ""
            responses.append(response)
        Response.objects.bulk_update(responses, ["form_data", "cached_key_fields", "ip_address"], batch_size=500)
        count += len(responses)

    return f"pseudonymized {count}"


RULES: list[Rule] = [
    # Credentials and one-time secrets
    delete_all("sessions.Session"),
    delete_all("oauth2_provider.AccessToken"),
    delete_all("oauth2_provider.RefreshToken"),
    delete_all("oauth2_provider.IDToken"),
    delete_all("oauth2_provider.Grant"),
    delete_all("oauth2_provider.DeviceGrant"),
    update("oauth2_provider.Application", client_secret=Value("")),
    delete_all("core.EmailVerificationToken"),
    delete_all("core.PasswordResetToken"),
    delete_all("tickets_v2.OrderCancellationToken"),
    delete_all("desuprofile_integration.ConfirmationCode"),
    delete_all("access.SMTPPassword"),
    delete_all("forms.KeyPair"),
    update("payments.PaymentsOrganizationMeta", checkout_password=Value("")),
    update("lippukala.Code", code=numbered("pseudonymized"), literate_code=Value("")),
    update("paikkala.Ticket", name=Value(""), email=Value(""), phone=Value(""), key=LPad(numbered(""), 8, Value("0"))),
    # Queued tasks may send email to real addresses when a developer starts a worker.
    delete_all("task_queue.QueuedTask"),
    # Persons first: the rules after this one copy their pseudonymized names.
    update(
        "core.Person",
        first_name=numbered("Person"),
        official_first_names=numbered("Person"),
        surname=Value("Testinen"),
        nick=unless_blank("nick", numbered("person")),
        discord_handle=unless_blank("discord_handle", numbered("person")),
        email=numbered("person", "@example.com"),
        # Finnish numbers never start with 000, so nobody gets called or texted by accident.
        phone=Concat(Value("+358000"), LPad(numbered(""), 7, Value("0"))),
        muncipality=Value("Testilä"),
        notes=Value(""),
        birth_date=TruncYear("birth_date"),
    ),
    update(
        "auth.User",
        username=numbered("user"),
        first_name=Coalesce(user_person("first_name"), Value("")),
        last_name=Coalesce(user_person("surname"), Value("")),
        email=Coalesce(user_person("email"), Value("")),
        password=Value(UNUSABLE_PASSWORD),
    ),
    update(
        "badges.Badge",
        first_name=Coalesce(person_of("person_id", "first_name"), Value("Badge")),
        surname=Coalesce(person_of("person_id", "surname"), Value("Testinen")),
        nick=unless_blank("nick", Coalesce(person_of("person_id", "nick"), Value(""))),
        notes=Value(""),
    ),
    # Admin log entries name the objects edited, and event log entries record request details.
    delete_all("admin.LogEntry"),
    remove_json_keys(
        "event_log_v2.Entry",
        "other_fields",
        ["ip_address", "context", "search_term", "user", "feedback_message"],
    ),
    delete_all("event_log.Entry"),
    update("desuprofile_integration.Connection", desuprofile_username=numbered("desuprofile")),
    update("labour.Signup", notes=Value("")),
    update("labour.Shift", notes=Value("")),
    *(signup_extra_rule(model) for model in signup_extra_models()),
    update("involvement.Invitation", email=numbered("invitation-", "@example.com")),
    update("membership.Membership", message=Value("")),
    Rule(
        "forms.Response",
        frozenset({"form_data", "cached_key_fields", "ip_address"}),
        pseudonymize_responses,
    ),
    update("messages_v2.MessageRecipient", email=numbered("recipient-", "@example.com"), subject=Value(REDACTED)),
    update("messages_v2.MessageBody", text=Value(REDACTED)),
    delete_all("mailings.PersonMessage"),
    delete_all("mailings.PersonMessageSubject"),
    delete_all("mailings.PersonMessageBody"),
    delete_all("access.EmailAlias"),
    update("access.InternalEmailAlias", target_emails=Value("")),
    update(
        "tickets_v2.Order",
        first_name=Value("Order"),
        last_name=Value("Testinen"),
        email=numbered("order", "@example.com", field="order_number"),
        phone=Value(""),
    ),
    update("tickets_v2.Receipt", email=Value("")),
    update("tickets_v2.PaymentStamp", data=Value({}, output_field=models.JSONField())),
    update(
        "tickets.Customer",
        first_name=Value("Customer"),
        last_name=Value("Testinen"),
        email=numbered("customer", "@example.com"),
        phone_number=Value(""),
    ),
    update("payments.CheckoutPayment", customer=Value({}, output_field=models.JSONField())),
    update("tickets.Order", ip_address=Value("")),
    update("lippukala.Order", address_text=Value(""), free_text=Value(""), comment=Value("")),
    update(
        "programme.Programme",
        notes=Value(""),
        notes_from_host=Value(""),
        solmukohta2024_other_emails=Value(""),
    ),
    delete_all("programme.ProgrammeFeedback"),
]


# Fields `is_suspicious` flags that were reviewed and hold no personal data or secrets.
NOT_PERSONAL: dict[str, frozenset[str]] = {
    label: frozenset(fields.split())
    for label, fields in {
        # Configuration written by organizers or administrators
        "auth.Permission": "codename",
        "oauth2_provider.Application": "client_id redirect_uris post_logout_redirect_uris name allowed_origins",
        "core.Organization": "muncipality",
        "access.CBACEntry": "claims",
        "access.InternalEmailAlias": "email_address",
        "access.SMTPServer": "ssh_username password_file_path_on_server",
        "intra.Team": "email",
        "labour.LabourEventMeta": "monitor_email contact_email",
        "labour.PersonnelClass": "perks",
        "program_v2.ProgramV2EventMeta": "contact_email",
        "tickets_v2.TicketsV2EventMeta": "contact_email",
        "programme.ProgrammeEventMeta": "contact_email",
        "tickets.TicketsEventMeta": "contact_email",
        "tickets.Product": "notify_email code",
        "programme.AlternativeProgrammeForm": "programme_form_code v2_dimensions",
        "programme.Category": "notes v2_dimensions",
        "programme.Room": "notes v2_dimensions",
        "programme.Role": "perks",
        "programme.SpecialReservation": "code",
        "programme.Tag": "v2_dimensions",
        "dimensions.UniverseAnnotation": "form_fields",
        "involvement.InvolvementToGroupMapping": "required_dimensions",
        "involvement.InvolvementToBadgeMapping": "required_dimensions annotations",
        "badges.SurveyToBadgeMapping": "required_dimensions annotations",
        "event_log_v2.Entry": "entry_type",
        "event_log_v2.Subscription": "entry_type",
        "forms.Survey": "slug cached_key_fields cached_default_response_dimensions cached_default_involvement_dimensions",
        "forms.Form": "title description thank_you_message fields cached_enriched_fields",
        "forms.Projection": (
            "default_language_code splats required_dimensions projected_dimensions filterable_dimensions"
            " order_by special_fields"
        ),
        # Organizers write these to many recipients at once, so they are not about any one person.
        "messages_v2.Message": "subject body recipient_filters",
        "messages_v2.MessageReplyTo": "email",
        # Programs, including their hosts, are published on the public schedule.
        "program_v2.Program": (
            "title slug description annotations cached_dimensions cached_combined_dimensions cached_color"
        ),
        "program_v2.ScheduleItem": (
            "cached_dimensions cached_combined_dimensions cached_location annotations cached_combined_annotations"
        ),
        # Roles, perks and dimensions that organizers assign
        "involvement.Invitation": "cached_dimensions",
        "involvement.Involvement": "title cached_dimensions annotations",
        "messages_v2.MessageRecipient": "cached_dimensions",
        "forms.Response": "cached_dimensions",
        "labour.Signup": "xxx_interim_shifts job_title override_formatted_perks",
        "labour.ArchivedSignup": "job_title",
        "badges.Badge": "job_title perks",
        "intra.TeamMember": "override_job_title",
        "programme.ProgrammeRole": "override_perks",
        "paikkala.Ticket": "qualifier_text_cache",
        "tickets_v2.Order": "product_data",
        "payments.CheckoutPayment": "items",
    }.items()
}


def find_orphan_tables() -> list[str]:
    """
    Tables that no installed model owns, such as those left behind by removed apps. No rule can
    cover them, and they may hold personal data.
    """
    known_tables = set(connection.introspection.django_table_names(include_views=False)) | {"django_migrations"}
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.relname
            FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = current_schema() AND c.relkind IN ('r', 'p') AND NOT c.relispartition
            ORDER BY c.relname
            """
        )
        return [table for (table,) in cursor.fetchall() if table not in known_tables]


def drop_orphan_tables() -> str:
    tables = find_orphan_tables()
    with connection.cursor() as cursor:
        for table in tables:
            cursor.execute(f"DROP TABLE {connection.ops.quote_name(table)} CASCADE")
    return f"dropped {', '.join(tables) or 'nothing'}"


def pseudonymize() -> Iterable[tuple[str, str]]:
    """Applies every rule in order, yielding the model label and a summary as each finishes."""
    yield "orphan tables", drop_orphan_tables()
    for rule in RULES:
        yield rule.model_label, rule.apply(rule.model)


PERSONAL_FIELD_NAME = re.compile(
    r"e_?mail|phone|first_name|surname|last_name|full_name|nick|address|(^|_)ip($|_)|token|secret|password"
    r"|hetu|ssn|identification|birth|diet|allerg|notes?$|handle|city|zip|muncipality|iban|key|code|username",
    re.IGNORECASE,
)
TEXT_LIKE_FIELDS = (
    models.CharField,
    models.TextField,
    models.JSONField,
    models.BinaryField,
    models.GenericIPAddressField,
    HStoreField,
    ArrayField,
)


def is_linked_to_person(model: type[models.Model]) -> bool:
    person_models = (Person, apps.get_model("auth.User"))
    return model in person_models or any(
        field.is_relation and field.related_model in person_models for field in model._meta.concrete_fields
    )


def is_suspicious(model: type[models.Model], field: models.Field) -> bool:
    """
    Could this field hold personal data or a secret? Free text on a row about a person could hold
    anything, so every such field is suspicious. Elsewhere only fields named like personal data are.
    """
    if field.primary_key or field.choices or isinstance(field, (models.SlugField, models.UUIDField)):
        return False
    if isinstance(field, models.DateField) and not isinstance(field, models.DateTimeField):
        return bool(PERSONAL_FIELD_NAME.search(field.name))
    if not isinstance(field, TEXT_LIKE_FIELDS):
        return False
    return (
        isinstance(field, models.JSONField)
        or is_linked_to_person(model)
        or bool(PERSONAL_FIELD_NAME.search(field.name))
    )


def managed_models() -> Iterable[type[models.Model]]:
    for model in apps.get_models():
        if model._meta.managed and not model._meta.proxy:
            yield model


def find_unclassified_fields() -> list[str]:
    covered: dict[str, frozenset[str]] = {}
    for rule in RULES:
        covered[rule.model_label] = covered.get(rule.model_label, frozenset()) | rule.fields

    unclassified = []
    for model in managed_models():
        label = model._meta.label
        rule_fields = covered.get(label, frozenset())
        if rule_fields == ALL_FIELDS:
            continue
        reviewed_fields = rule_fields | NOT_PERSONAL.get(label, frozenset())
        unclassified.extend(
            f"{label}.{field.name}"
            for field in model._meta.concrete_fields
            if field.name not in reviewed_fields and is_suspicious(model, field)
        )

    return unclassified


def find_stale_classifications() -> list[str]:
    """Rules and `NOT_PERSONAL` entries that name a model or field that no longer exists."""
    classified = [(rule.model_label, rule.fields - ALL_FIELDS) for rule in RULES] + list(NOT_PERSONAL.items())

    stale = []
    for label, field_names in classified:
        try:
            model = apps.get_model(label)
        except LookupError:
            stale.append(label)
            continue
        existing = {field.name for field in model._meta.concrete_fields}
        stale.extend(f"{label}.{name}" for name in sorted(field_names - existing))

    return stale
