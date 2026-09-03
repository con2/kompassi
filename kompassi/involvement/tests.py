from datetime import datetime, timedelta

import pytest
from django.test import RequestFactory
from django.utils.timezone import now

from kompassi.access.models.cbac_entry import CBACEntry
from kompassi.core.models.enums import ProgramRoleRetentionPolicy
from kompassi.core.models.event import Event
from kompassi.core.models.person import Person
from kompassi.core.utils.cleanup import perform_cleanup
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO
from kompassi.dimensions.models.enums import AnnotationDataType, DimensionApp
from kompassi.dimensions.models.universe_annotation import UniverseAnnotation
from kompassi.event_log_v2.models.entry import Entry

from .emperkelators.desucon2026 import DesuconEmperkelator
from .emperkelators.ropecon2026 import RopeconEmperkelator
from .emperkelators.tracon2026 import Perks as TraconPerks
from .emperkelators.tracon2026 import TicketType as TraconTicketType
from .emperkelators.tracon2026 import TraconEmperkelator
from .models.enums import InvolvementType
from .models.involvement import Involvement
from .models.meta import InvolvementEventMeta
from .perks import (
    MANUAL_PERKS_OVERRIDE_SLUG,
    annotation_override_value,
    dimension_override_value,
    get_manual_perks_override_dimension,
    get_perk_keys,
)


@pytest.mark.parametrize(
    "annotation_slug,expected",
    [
        ("tracon:mealVouchers", "a-tracon-meal-vouchers"),
        ("tracon:swag", "a-tracon-swag"),
        ("tracon:extraSwag", "a-tracon-extra-swag"),
        ("internal:overrideBadgeJobTitle", "a-internal-override-badge-job-title"),
    ],
)
def test_annotation_override_value(annotation_slug: str, expected: str):
    assert annotation_override_value(annotation_slug) == expected


def test_dimension_override_value():
    assert dimension_override_value("ticket-type") == "d-ticket-type"


def _setup_perk_universe():
    """Set up a dummy involvement universe with one dimension perk and one annotation perk."""
    meta, _ = InvolvementEventMeta.get_or_create_dummy()
    universe = meta.universe

    DimensionDTO(
        slug="ticket-type",
        title=dict(en="Ticket type"),
        choices=[
            DimensionValueDTO(slug="basic", title=dict(en="Basic")),
            DimensionValueDTO(slug="vip", title=dict(en="VIP")),
        ],
    ).save(universe)

    annotations = AnnotationDTO.save_many(
        [
            AnnotationDTO(
                slug="tracon:mealVouchers",
                title=dict(en="Meal vouchers"),
                type=AnnotationDataType.NUMBER,
                is_perk=True,
                is_applicable_to_involvements=True,
                is_applicable_to_program_items=False,
            )
        ]
    )
    UniverseAnnotation.ensure(universe, annotations)

    get_manual_perks_override_dimension().save(universe)

    return universe


@pytest.mark.django_db
def test_get_perk_keys():
    universe = _setup_perk_universe()

    perk_keys = get_perk_keys(universe)

    assert perk_keys["d-ticket-type"].kind == "dimension"
    assert perk_keys["d-ticket-type"].slug == "ticket-type"
    assert perk_keys["a-tracon-meal-vouchers"].kind == "annotation"
    assert perk_keys["a-tracon-meal-vouchers"].slug == "tracon:mealVouchers"

    # technical dimensions are not perks
    assert "d-app" not in perk_keys
    assert "d-type" not in perk_keys
    assert f"d-{MANUAL_PERKS_OVERRIDE_SLUG}" not in perk_keys


@pytest.mark.django_db
def test_preserve_manual_perk_overrides():
    universe = _setup_perk_universe()

    existing = Involvement(
        cached_dimensions={
            MANUAL_PERKS_OVERRIDE_SLUG: ["d-ticket-type", "a-tracon-meal-vouchers"],
            "ticket-type": ["vip"],
        },
        annotations={"tracon:mealVouchers": 3},
    )

    # Automatically computed values that should be overridden by the manual ones.
    dimension_values = {"ticket-type": ["basic"]}
    annotation_values = {"tracon:mealVouchers": 1, "internal:formattedPerks": "auto"}

    Involvement._preserve_manual_perk_overrides(universe, existing, dimension_values, annotation_values)

    assert dimension_values["ticket-type"] == ["vip"]
    assert annotation_values["tracon:mealVouchers"] == 3
    # non-overridden computed values are left untouched
    assert annotation_values["internal:formattedPerks"] == "auto"


@pytest.mark.django_db
def test_non_overridden_perks_are_not_preserved():
    universe = _setup_perk_universe()

    existing = Involvement(
        cached_dimensions={MANUAL_PERKS_OVERRIDE_SLUG: [], "ticket-type": ["vip"]},
        annotations={"tracon:mealVouchers": 3},
    )

    dimension_values = {"ticket-type": ["basic"]}
    annotation_values = {"tracon:mealVouchers": 1}

    Involvement._preserve_manual_perk_overrides(
        universe,
        existing,
        dimension_values,
        annotation_values,  # type: ignore
    )

    # With no overrides recorded, the automatically computed values stand.
    assert dimension_values["ticket-type"] == ["basic"]
    assert annotation_values["tracon:mealVouchers"] == 1


def test_tracon_get_formatted_perks_computed():
    dimension_values = {"ticket-type": ["internal-badge"], "shirt-size": ["unisex-l"]}
    annotation_values = {"tracon:mealVouchers": 2, "tracon:swag": True, "tracon:extraSwag": False}

    assert (
        TraconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Badge (internal), 2 ruokalippua, L Unisex"
    )


def test_tracon_get_formatted_perks_no_meals_no_swag():
    dimension_values = {"ticket-type": []}
    annotation_values = {"tracon:mealVouchers": 0, "tracon:swag": False, "tracon:extraSwag": False}

    assert (
        TraconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Ei lippuetua, ei ruokalippuja, ei työvoimatuotetta"
    )


def test_tracon_get_formatted_perks_extra_swag():
    dimension_values = {"ticket-type": ["super-internal-badge"], "shirt-size": ["ladyfit-xs"]}
    annotation_values = {"tracon:mealVouchers": 4, "tracon:swag": True, "tracon:extraSwag": True}

    assert (
        TraconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Badge (super internal), 4 ruokalippua, XS Ladyfit, ekstramuki"
    )


def test_tracon_get_formatted_perks_override():
    dimension_values = {"ticket-type": ["internal-badge"]}
    annotation_values = {
        "tracon:mealVouchers": 2,
        "internal:overrideFormattedPerks": "Tässä voi lukea ihan mitä hyvänsä",
    }

    assert (
        TraconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Tässä voi lukea ihan mitä hyvänsä"
    )


def test_desucon_get_formatted_perks_computed():
    dimension_values = {"shirt-type": ["staff"], "shirt-size": ["m-unisex"]}
    annotation_values = {"tracon:mealVouchers": 1}

    assert (
        DesuconEmperkelator.get_formatted_perks(
            dimension_values,
            annotation_values,  # type: ignore
        )
        == "STAFF-paita (M Unisex), 1 ruokalippu"
    )


def test_desucon_get_formatted_perks_no_shirt():
    dimension_values = {}
    annotation_values = {"tracon:mealVouchers": 2}

    assert (
        DesuconEmperkelator.get_formatted_perks(
            dimension_values,
            annotation_values,  # type: ignore
        )
        == "Ei paitaa, 2 ruokalippua"
    )


def test_desucon_get_formatted_perks_override():
    dimension_values = {"shirt-type": ["staff"], "shirt-size": ["m-unisex"]}
    annotation_values = {"tracon:mealVouchers": 1, "internal:overrideFormattedPerks": "Custom perks"}

    assert DesuconEmperkelator.get_formatted_perks(dimension_values, annotation_values) == "Custom perks"


def test_ropecon_get_formatted_perks_computed():
    dimension_values = {"ticket-type": ["weekend-ticket"], "v1-personnel-class": ["conitea"]}
    annotation_values = {"tracon:mealVouchers": 2}

    assert (
        RopeconEmperkelator.get_formatted_perks(
            dimension_values,
            annotation_values,  # type: ignore
        )
        == "Viikonloppulippu, coniteabadge, 2\xa0ruokalippua"
    )


def test_ropecon_get_formatted_perks_single_meal():
    dimension_values = {"ticket-type": ["day-ticket"], "v1-personnel-class": ["ohjelma"]}
    annotation_values = {"tracon:mealVouchers": 1}

    assert (
        RopeconEmperkelator.get_formatted_perks(
            dimension_values,
            annotation_values,  # type: ignore
        )
        == "Päivälippu, ohjelmabadge, 1\xa0ruokalippu"
    )


def test_ropecon_get_formatted_perks_override():
    dimension_values = {"ticket-type": ["day-ticket"]}
    annotation_values = {"tracon:mealVouchers": 1, "internal:overrideFormattedPerks": "Custom override"}

    assert RopeconEmperkelator.get_formatted_perks(dimension_values, annotation_values) == "Custom override"


@pytest.mark.django_db
def test_for_combined_perks_respects_manual_perk_override():
    """
    Regression test: a manually overridden perk must be reflected in the
    internal:formattedPerks stored on the recomputed combined perks involvement,
    not the auto-computed value that TraconEmperkelator would otherwise produce.
    """
    from kompassi.labour.models.labour_event_meta import LabourEventMeta
    from kompassi.labour.models.personnel_class import PersonnelClass

    person, _ = Person.get_or_create_dummy()
    event, _ = Event.get_or_create_dummy(name="Formatted Perks Test 2099")
    event.slug = "tracon2099"
    event.save(update_fields=["slug"])

    # TraconEmperkelator only registers the v1-personnel-class dimension (and the
    # PROGRAM_HOST involvement path hardcodes its value to "ohjelma") if the event
    # has a LabourEventMeta and a matching PersonnelClass.
    LabourEventMeta.get_or_create_dummy(event=event)
    PersonnelClass.objects.create(event=event, name="Ohjelma", slug="ohjelma", app_label="program_v2")

    # ensure() registers the "registry" dimension's values from the scope's existing
    # registries before it creates the default "volunteers" registry, so the first
    # call never has "volunteers" as a choice. Calling it again picks it up.
    InvolvementEventMeta.ensure(event)
    meta = InvolvementEventMeta.ensure(event)
    universe = meta.universe

    # An active involvement so for_combined_perks has something to compute from.
    # Perks.for_program_host always grants INTERNAL_BADGE, regardless of the
    # involvement's program/response.
    Involvement.objects.create(
        universe=universe,
        person=person,
        app=DimensionApp.PROGRAM,
        type=InvolvementType.PROGRAM_HOST,
        registry=meta.default_registry,
        is_active=True,
    )

    # Existing combined perks with ticket-type manually overridden to a higher tier
    # than what the auto-computation (INTERNAL_BADGE) would produce.
    Involvement.objects.create(
        universe=universe,
        person=person,
        app=DimensionApp.INVOLVEMENT,
        type=InvolvementType.COMBINED_PERKS,
        registry=meta.default_registry,
        is_active=True,
        cached_dimensions={
            MANUAL_PERKS_OVERRIDE_SLUG: [dimension_override_value("ticket-type")],
            "ticket-type": ["super-internal-badge"],
        },
    )

    result = Involvement.for_combined_perks(event, person)

    assert result is not None
    assert result.cached_dimensions["ticket-type"] == ["super-internal-badge"]

    formatted_perks = result.annotations["internal:formattedPerks"]
    assert "Badge (super internal)" in formatted_perks
    assert "Badge (internal)," not in formatted_perks


def test_tracon_program_host_ticket_type_set_on_involvement():
    """
    A program manager may set the ticket-type dimension on a single program host
    involvement to grant less than the default INTERNAL_BADGE.
    """
    involvement = Involvement(
        type=InvolvementType.PROGRAM_HOST,
        cached_dimensions={"ticket-type": ["free-ticket-saturday"]},
    )

    perks = TraconPerks.for_program_host(involvement)

    assert perks.ticket_type == TraconTicketType.FREE_TICKET_SATURDAY
    assert perks.meals == 1
    assert perks.swag


def test_tracon_program_host_unknown_ticket_type_falls_back_to_default():
    involvement = Involvement(type=InvolvementType.PROGRAM_HOST, cached_dimensions={"ticket-type": ["no-such-type"]})

    perks = TraconPerks.for_program_host(involvement)

    assert perks.ticket_type == TraconTicketType.INTERNAL_BADGE


@pytest.mark.django_db
def test_for_combined_perks_uses_program_host_ticket_type():
    """
    Regression test: the ticket type a program manager sets on a program host
    involvement must carry over to the combined perks, both as the ticket-type
    dimension and in internal:formattedPerks.
    """
    from kompassi.labour.models.labour_event_meta import LabourEventMeta
    from kompassi.labour.models.personnel_class import PersonnelClass

    person, _ = Person.get_or_create_dummy()
    event, _ = Event.get_or_create_dummy(name="Program Host Ticket Type Test 2099")
    event.slug = "tracon2099"
    event.save(update_fields=["slug"])

    LabourEventMeta.get_or_create_dummy(event=event)
    PersonnelClass.objects.create(event=event, name="Ohjelma", slug="ohjelma", app_label="program_v2")

    InvolvementEventMeta.ensure(event)
    meta = InvolvementEventMeta.ensure(event)
    universe = meta.universe

    Involvement.objects.create(
        universe=universe,
        person=person,
        app=DimensionApp.PROGRAM,
        type=InvolvementType.PROGRAM_HOST,
        registry=meta.default_registry,
        is_active=True,
        cached_dimensions={"ticket-type": ["free-ticket-saturday"]},
    )

    result = Involvement.for_combined_perks(event, person)

    assert result is not None
    assert result.cached_dimensions["ticket-type"] == ["free-ticket-saturday"]

    formatted_perks = result.annotations["internal:formattedPerks"]
    assert "Vapaalippu lauantai" in formatted_perks
    assert "Badge" not in formatted_perks


def _perform_retention_cleanup():
    """perform_cleanup emits event log entries, which need the current month's partition."""
    Entry.ensure_partitions()
    perform_cleanup()


def _make_retention_involvement(
    *,
    slug: str,
    involvement_type: InvolvementType = InvolvementType.SURVEY_RESPONSE,
    default_retention_period: timedelta | None = timedelta(days=365),
    end_time: datetime | None = None,
    program_role_retention_policy: ProgramRoleRetentionPolicy | None = None,
):
    """
    An involvement wired so that retention cleanup has everything it needs. Each call gets
    its own event, registry and person, so that cases within one test, which differ
    precisely in these, do not overwrite each other.
    """
    from kompassi.core.models.organization import Organization
    from kompassi.core.models.venue import Venue
    from kompassi.dimensions.models.universe import Universe

    from .models.registry import Registry

    organization, _created = Organization.get_or_create_dummy()
    venue, _created = Venue.get_or_create_dummy()
    event = Event.objects.create(
        name=f"Retention test event {slug}",
        slug=f"retention-{slug}",
        organization=organization,
        venue=venue,
        start_time=(end_time or now()) - timedelta(days=1),
        end_time=end_time,
    )

    registry = Registry.objects.create(
        scope=organization.scope,
        slug=f"retention-{slug}",
        title_en=f"Retention test registry {slug}",
        default_retention_period=default_retention_period,
    )

    universe = Universe.objects.create(
        scope=event.scope,
        slug=f"retention-{slug}",
        app=DimensionApp.INVOLVEMENT,
    )

    person = Person.objects.create(
        first_name="Retention",
        surname=slug,
        email=f"retention-{slug}@example.com",
        program_role_retention_policy=program_role_retention_policy,
    )

    return Involvement.objects.create(
        universe=universe,
        person=person,
        app=DimensionApp.INVOLVEMENT,
        type=involvement_type,
        registry=registry,
        is_active=True,
    )


@pytest.mark.django_db
def test_involvement_retention_registry_default():
    """
    An involvement is deleted once its registry's default retention period has passed since
    the end time of the event. A registry without a retention period retains indefinitely,
    and the anchor falls back to the creation time when the event has no end time.
    """
    expired = _make_retention_involvement(
        slug="expired",
        end_time=now() - timedelta(days=400),
    )
    unexpired = _make_retention_involvement(
        slug="unexpired",
        end_time=now() - timedelta(days=300),
    )
    no_retention = _make_retention_involvement(
        slug="no-retention",
        default_retention_period=None,
        end_time=now() - timedelta(days=4000),
    )
    # No end time: the anchor is created_at, which is right now, so this is not expired.
    no_end_time = _make_retention_involvement(slug="no-end-time", end_time=None)

    _perform_retention_cleanup()

    assert not Involvement.objects.filter(pk=expired.pk).exists()
    assert Involvement.objects.filter(pk=unexpired.pk).exists()
    assert Involvement.objects.filter(pk=no_retention.pk).exists()
    assert Involvement.objects.filter(pk=no_end_time.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "policy,expect_deleted",
    [
        (None, False),
        (ProgramRoleRetentionPolicy.RETAIN, False),
        (ProgramRoleRetentionPolicy.REMOVE, True),
    ],
)
def test_involvement_retention_program_host_policy(policy, expect_deleted):
    """
    Program hosts are often proud of their program history, so an expired PROGRAM_HOST
    involvement is only deleted when the person has explicitly chosen REMOVE. NULL (no
    conscious choice) and RETAIN both keep it.
    """
    involvement = _make_retention_involvement(
        slug=f"program-host-{policy.name.lower() if policy else 'unset'}",
        involvement_type=InvolvementType.PROGRAM_HOST,
        end_time=now() - timedelta(days=400),
        program_role_retention_policy=policy,
    )

    _perform_retention_cleanup()

    assert Involvement.objects.filter(pk=involvement.pk).exists() is not expect_deleted


@pytest.mark.django_db
def test_involvement_retention_revokes_badge():
    """
    An expiring involvement is deactivated and its dependents refreshed before the row goes
    away, so that the badge it granted is revoked rather than left behind.
    """
    from kompassi.badges.models.badge import Badge
    from kompassi.badges.models.badges_event_meta import BadgesEventMeta
    from kompassi.labour.models.personnel_class import PersonnelClass

    meta, _created = InvolvementEventMeta.get_or_create_dummy()
    event = meta.event
    event.end_time = now() - timedelta(days=400)
    event.save(update_fields=["end_time"])

    BadgesEventMeta.get_or_create_dummy()
    personnel_class = PersonnelClass.objects.create(
        event=event,
        name="Ohjelma",
        slug="ohjelma",
        app_label="program_v2",
    )

    person, _created = Person.get_or_create_dummy()
    registry = meta.default_registry
    assert registry is not None
    registry.default_retention_period = timedelta(days=365)
    registry.save(update_fields=["default_retention_period"])

    involvement = Involvement.objects.create(
        universe=meta.universe,
        person=person,
        app=DimensionApp.INVOLVEMENT,
        type=InvolvementType.SURVEY_RESPONSE,
        registry=registry,
        is_active=True,
    )
    badge = Badge.objects.create(person=person, personnel_class=personnel_class)

    _perform_retention_cleanup()

    assert not Involvement.objects.filter(pk=involvement.pk).exists()
    assert not Badge.objects.filter(pk=badge.pk, revoked_at__isnull=True).exists()


@pytest.mark.django_db
def test_involvement_survives_expired_response():
    """
    Involvement retention comes from the registry while a survey may override retention of
    its responses, so the response of an unexpired involvement can expire first. The
    involvement then survives with response=None (SET_NULL).
    """
    from kompassi.forms.models.form import Form
    from kompassi.forms.models.response import Response
    from kompassi.forms.models.survey import Survey

    involvement = _make_retention_involvement(
        slug="unexpired-with-expired-response",
        involvement_type=InvolvementType.PROGRAM_HOST,
        end_time=now() - timedelta(days=100),
    )
    event = involvement.universe.scope.event
    assert event is not None

    survey = Survey.objects.create(
        event=event,
        slug="expiring-fast",
        registry=involvement.registry,
        retention_period=timedelta(days=30),
    )
    form = Form.objects.create(
        event=event,
        survey=survey,
        language="en",
        fields=[dict(slug="title", type="SingleLineText")],
    )
    response = Response.objects.create(form=form, form_data=dict(title="Personal data"))
    involvement.response = response
    involvement.save(update_fields=["response"])

    _perform_retention_cleanup()

    assert not Response.objects.filter(pk=response.pk).exists()

    involvement.refresh_from_db()
    assert involvement.response is None


def _graphql_request(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    return request


def _make_org_with_two_events(prefix: str):
    """
    Two events of one organization, both with an ensured InvolvementEventMeta, so that
    org-scoped CBAC and org-wide registry dimension refresh have something to bite on.
    """
    from kompassi.core.models.organization import Organization
    from kompassi.core.models.venue import Venue

    organization, _created = Organization.get_or_create_dummy()
    venue, _created = Venue.get_or_create_dummy()

    def make_event(slug: str) -> Event:
        return Event.objects.create(
            name=f"Registry admin test event {slug}",
            slug=slug,
            organization=organization,
            venue=venue,
            start_time=now(),
            end_time=now() + timedelta(days=1),
        )

    event1 = make_event(f"{prefix}-1")
    event2 = make_event(f"{prefix}-2")

    meta1 = InvolvementEventMeta.ensure(event1)
    meta2 = InvolvementEventMeta.ensure(event2)

    return organization, event1, meta1, event2, meta2


REGISTRIES_QUERY = """
  query Registries($eventSlug: String!) {
    event(slug: $eventSlug) {
      involvement {
        registries {
          slug
          canRemove
        }
      }
    }
  }
"""

CREATE_REGISTRY_MUTATION = """
  mutation CreateRegistry($input: CreateRegistryInput!) {
    createRegistry(input: $input) {
      registry {
        slug
        titleEn
        titleFi
        titleSv
      }
    }
  }
"""

UPDATE_REGISTRY_MUTATION = """
  mutation UpdateRegistry($input: UpdateRegistryInput!) {
    updateRegistry(input: $input) {
      registry {
        slug
        titleEn
        defaultRetentionPeriodDays
      }
    }
  }
"""

DELETE_REGISTRY_MUTATION = """
  mutation DeleteRegistry($input: DeleteRegistryInput!) {
    deleteRegistry(input: $input) {
      slug
    }
  }
"""


@pytest.mark.django_db
def test_registry_admin_cbac_is_org_scoped():
    """
    Registries hang off the organization, not the event, so an involvement admin of
    *any* event of the org can list, create and update registries of the org -- the
    existing {organization, app} grant (event deliberately omitted, see
    CBACEntry.ensure_admin_group_privileges_for_event) matches an org-scope claim.
    """
    from kompassi.graphql_api.schema import schema

    Entry.ensure_partitions()

    _organization, event1, meta1, event2, _meta2 = _make_org_with_two_events("registry-cbac-org")
    person, _created = Person.get_or_create_dummy()
    assert person.user

    meta1.admin_group.user_set.add(person.user)
    CBACEntry.ensure_admin_group_privileges_for_event(event1)

    request = _graphql_request(person.user)

    # Admin of event1 can see registries via event2 -- a *different* event of the same org.
    result = schema.execute(REGISTRIES_QUERY, None, request, variable_values=dict(eventSlug=event2.slug))
    assert not result.errors
    assert result.data is not None
    slugs = {r["slug"] for r in result.data["event"]["involvement"]["registries"]}
    assert "volunteers" in slugs

    # createRegistry and updateRegistry are likewise allowed.
    create_result = schema.execute(
        CREATE_REGISTRY_MUTATION,
        None,
        request,
        variable_values=dict(
            input=dict(
                eventSlug=event2.slug,
                formData=dict(
                    slug="press",
                    titleEn="Press",
                    titleFi="Lehdistö",
                    titleSv="Press",
                ),
            )
        ),
    )
    assert not create_result.errors
    assert create_result.data["createRegistry"]["registry"]["slug"] == "press"

    update_result = schema.execute(
        UPDATE_REGISTRY_MUTATION,
        None,
        request,
        variable_values=dict(
            input=dict(
                eventSlug=event1.slug,
                registrySlug="press",
                formData=dict(
                    titleEn="Press corps",
                    titleFi="Lehdistö",
                    titleSv="Press",
                    defaultRetentionPeriodDays=30,
                ),
            )
        ),
    )
    assert not update_result.errors
    assert update_result.data["updateRegistry"]["registry"]["titleEn"] == "Press corps"
    assert update_result.data["updateRegistry"]["registry"]["defaultRetentionPeriodDays"] == 30


@pytest.mark.django_db
def test_registry_admin_denies_event_scoped_grant():
    """
    A grant that (unlike the standard admin group privilege grant) includes an `event`
    claim does not match an org-scope request, because CBACEntry.is_allowed requires the
    granted claims to be a *subset* of the request claims, and the request claims for an
    org-scope check have no `event` key at all for the grant to be a subset of.
    """
    from kompassi.graphql_api.schema import schema

    Entry.ensure_partitions()

    organization, event1, _meta1, _event2, _meta2 = _make_org_with_two_events("registry-cbac-event-scoped")
    person, _created = Person.get_or_create_dummy()
    assert person.user

    CBACEntry.objects.create(
        user=person.user,
        claims={
            "organization": organization.slug,
            "event": event1.slug,
            "app": "involvement",
        },
        valid_from=now(),
        valid_until=now() + timedelta(days=1),
    )

    request = _graphql_request(person.user)
    result = schema.execute(REGISTRIES_QUERY, None, request, variable_values=dict(eventSlug=event1.slug))
    assert result.errors


@pytest.mark.django_db
def test_update_registry_cannot_change_slug():
    """
    UpdateRegistryForm has no `slug` field at all, so even if a client sends one in
    formData, it is silently ignored rather than applied.
    """
    from kompassi.graphql_api.schema import schema

    from .models.registry import Registry

    Entry.ensure_partitions()

    organization, event1, meta1, _event2, _meta2 = _make_org_with_two_events("registry-slug-immutable")
    person, _created = Person.get_or_create_dummy()
    assert person.user
    meta1.admin_group.user_set.add(person.user)
    CBACEntry.ensure_admin_group_privileges_for_event(event1)

    request = _graphql_request(person.user)
    result = schema.execute(
        UPDATE_REGISTRY_MUTATION,
        None,
        request,
        variable_values=dict(
            input=dict(
                eventSlug=event1.slug,
                registrySlug="volunteers",
                formData=dict(
                    slug="hijacked",
                    titleEn="Volunteers",
                    titleFi="Vapaaehtoiset",
                    titleSv="Volontärer",
                ),
            )
        ),
    )
    assert not result.errors
    assert result.data["updateRegistry"]["registry"]["slug"] == "volunteers"
    assert not Registry.objects.filter(scope=organization.scope, slug="hijacked").exists()


@pytest.mark.django_db
def test_registry_dimension_refresh_on_create_and_delete():
    """
    The technical `registry` dimension enumerates the org's registries per event, so a
    new registry must appear as a dimension value in *every* event of the org, and a
    deleted one must be swept from all of them.
    """
    from kompassi.graphql_api.schema import schema

    Entry.ensure_partitions()

    _organization, event1, meta1, _event2, meta2 = _make_org_with_two_events("registry-dimension-refresh")
    person, _created = Person.get_or_create_dummy()
    assert person.user
    meta1.admin_group.user_set.add(person.user)
    CBACEntry.ensure_admin_group_privileges_for_event(event1)

    request = _graphql_request(person.user)

    def registry_dimension_slugs(meta: InvolvementEventMeta) -> set[str]:
        dimension = meta.universe.dimensions.get(slug="registry")
        return set(dimension.values.values_list("slug", flat=True))

    create_result = schema.execute(
        CREATE_REGISTRY_MUTATION,
        None,
        request,
        variable_values=dict(
            input=dict(
                eventSlug=event1.slug,
                formData=dict(slug="alumni", titleEn="Alumni", titleFi="Alumnit", titleSv="Alumner"),
            )
        ),
    )
    assert not create_result.errors

    assert "alumni" in registry_dimension_slugs(meta1)
    assert "alumni" in registry_dimension_slugs(meta2)

    delete_result = schema.execute(
        DELETE_REGISTRY_MUTATION,
        None,
        request,
        variable_values=dict(input=dict(eventSlug=event1.slug, registrySlug="alumni")),
    )
    assert not delete_result.errors

    assert "alumni" not in registry_dimension_slugs(meta1)
    assert "alumni" not in registry_dimension_slugs(meta2)


@pytest.mark.django_db
def test_registry_can_be_deleted_by_denies_while_referenced():
    """
    A registry cannot be deleted while anything -- an involvement, a survey, a badges
    event meta, or either app's default-registry setting -- still references it.
    """
    from kompassi.core.models.organization import Organization
    from kompassi.core.models.venue import Venue
    from kompassi.dimensions.models.universe import Universe
    from kompassi.forms.models.survey import Survey
    from kompassi.program_v2.models.meta import ProgramV2EventMeta

    from .models.registry import Registry

    Entry.ensure_partitions()

    organization, _created = Organization.get_or_create_dummy()
    venue, _created = Venue.get_or_create_dummy()
    event = Event.objects.create(
        name="Registry deletion guard test event",
        slug="registry-deletion-guard",
        organization=organization,
        venue=venue,
        start_time=now(),
        end_time=now() + timedelta(days=1),
    )

    meta = InvolvementEventMeta.ensure(event)
    person, _created = Person.get_or_create_dummy()
    assert person.user
    meta.admin_group.user_set.add(person.user)
    CBACEntry.ensure_admin_group_privileges_for_event(event)
    request = _graphql_request(person.user)

    registry = Registry.objects.create(
        scope=organization.scope,
        slug="deletion-guard-registry",
        title_en="Deletion guard registry",
    )
    assert registry.can_be_deleted_by(request)

    universe = Universe.objects.create(scope=event.scope, slug="deletion-guard", app=DimensionApp.INVOLVEMENT)
    involvement = Involvement.objects.create(
        universe=universe,
        person=person,
        app=DimensionApp.INVOLVEMENT,
        type=InvolvementType.SURVEY_RESPONSE,
        registry=registry,
        is_active=True,
    )
    assert not registry.can_be_deleted_by(request)
    involvement.delete()
    assert registry.can_be_deleted_by(request)

    survey = Survey.objects.create(event=event, slug="deletion-guard-survey", registry=registry)
    assert not registry.can_be_deleted_by(request)
    survey.delete()
    assert registry.can_be_deleted_by(request)

    meta = InvolvementEventMeta.ensure(event)
    meta.default_registry = registry
    meta.save(update_fields=["default_registry"])
    assert not registry.can_be_deleted_by(request)
    meta.default_registry = None
    meta.save(update_fields=["default_registry"])
    assert registry.can_be_deleted_by(request)

    program_meta, _created = ProgramV2EventMeta.objects.get_or_create(
        event=event,
        defaults=dict(admin_group=ProgramV2EventMeta.get_or_create_groups(event, ("admins",))[0]),
    )
    program_meta.default_registry = registry
    program_meta.save(update_fields=["default_registry"])
    assert not registry.can_be_deleted_by(request)
    program_meta.default_registry = None
    program_meta.save(update_fields=["default_registry"])
    assert registry.can_be_deleted_by(request)

    from kompassi.badges.models.badges_event_meta import BadgesEventMeta

    badges_meta, _created = BadgesEventMeta.objects.get_or_create(
        event=event,
        defaults=dict(admin_group=BadgesEventMeta.get_or_create_groups(event, ("admins",))[0]),
    )
    badges_meta.registry = registry
    badges_meta.save(update_fields=["registry"])
    assert not registry.can_be_deleted_by(request)
    badges_meta.registry = None
    badges_meta.save(update_fields=["registry"])
    assert registry.can_be_deleted_by(request)
