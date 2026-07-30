import pytest
from django.core import mail
from django.utils.timezone import now

from kompassi.core.graphql.profile_own import OwnProfileType
from kompassi.core.models.event import Event
from kompassi.core.models.person import Person
from kompassi.event_log_v2.models import Entry
from kompassi.event_log_v2.utils.emit import emit
from kompassi.involvement.models.enums import InvolvementApp, InvolvementType
from kompassi.involvement.models.involvement import Involvement
from kompassi.involvement.models.registry import Registry
from kompassi.program_v2.models.meta import ProgramV2EventMeta

from .models.enums import MessageDispatch, MessageState
from .models.message import Message
from .models.message_recipient import MessageRecipient

INJECTION_PAYLOAD = "[x](javascript:alert(1)) <img src=x onerror=alert(1)> **bold** # heading"


def _setup_event(name: str):
    """A ProgramV2EventMeta (and, transitively, InvolvementEventMeta) for a fresh dummy event."""
    event, _ = Event.get_or_create_dummy(name=name)
    registry, _ = Registry.get_or_create_dummy()

    meta, created = ProgramV2EventMeta.objects.get_or_create(
        event=event,
        defaults=dict(
            admin_group=ProgramV2EventMeta.get_or_create_groups(event, ("admins",))[0],
            is_accepting_feedback=True,
            contact_email="Messages Test <messages@example.com>",
            guide_v2_embedded_url="https://example.com/guide",
            default_registry=registry,
        ),
    )
    if created:
        meta.ensure()

    return event, meta


def _make_involvement(universe, person, registry, *, type, is_active, **extra_dimensions):
    cached_dimensions = {
        "app": [InvolvementApp.PROGRAM.value],
        "type": [type.value],
        "state": ["active"] if is_active else ["inactive"],
        "registry": [registry.slug],
        **extra_dimensions,
    }
    return Involvement.objects.create(
        universe=universe,
        person=person,
        app=InvolvementApp.PROGRAM,
        type=type,
        registry=registry,
        is_active=is_active,
        cached_dimensions=cached_dimensions,
    )


@pytest.mark.django_db
def test_compose_and_send_message():
    Entry.ensure_partitions()

    event, meta = _setup_event("Messages V2 Send Test")
    universe = event.involvement_universe
    registry = meta.default_registry

    offerer, _ = Person.get_or_create_dummy()
    offerer.first_name = "Ada"
    offerer.save()

    # Same rendered FIRST_NAME/EVENT_NAME as offerer -> exercises MessageBody dedup.
    host, _ = Person.get_or_create_dummy(another=True)
    host.first_name = "Ada"
    host.save()

    injected = Person.objects.create(first_name=INJECTION_PAYLOAD, surname="Payload", email="injected@example.com")
    wrong_category_host = Person.objects.create(first_name="Bob", surname="Wrong", email="wrong@example.com")
    inactive_host = Person.objects.create(first_name="Carl", surname="Inactive", email="inactive@example.com")

    _make_involvement(universe, offerer, registry, type=InvolvementType.PROGRAM_OFFER, is_active=True)
    _make_involvement(universe, injected, registry, type=InvolvementType.PROGRAM_OFFER, is_active=True)
    _make_involvement(
        universe, host, registry, type=InvolvementType.PROGRAM_HOST, is_active=True, category=["miniature-games"]
    )
    _make_involvement(
        universe,
        wrong_category_host,
        registry,
        type=InvolvementType.PROGRAM_HOST,
        is_active=True,
        category=["board-games"],
    )
    _make_involvement(
        universe,
        inactive_host,
        registry,
        type=InvolvementType.PROGRAM_HOST,
        is_active=False,
        category=["miniature-games"],
    )

    message = Message.objects.create(
        universe=universe,
        subject="Hello {FIRST_NAME}",
        body="Hi {FIRST_NAME}!\n\n**Welcome** to {EVENT_NAME}.\n\n# Important",
        dispatch=MessageDispatch.PER_PERSON,
        recipient_filters=[
            [{"dimension": "type", "values": ["program-offer"]}, {"dimension": "state", "values": ["active"]}],
            [
                {"dimension": "type", "values": ["program-host"]},
                {"dimension": "state", "values": ["active"]},
                {"dimension": "category", "values": ["miniature-games"]},
            ],
        ],
    )
    message.clean_recipient_filters()
    message.save()

    emit("messages_v2.message.created", event=event, other_fields=dict(message_id=message.id))

    assert message.state == MessageState.DRAFT
    assert message.resolve_recipient_count() == 3

    initial_recipients = message.resolve_recipient_count()
    message.send()

    emit(
        "messages_v2.message.sent",
        event=event,
        other_fields=dict(
            message_id=message.id,
            initial_recipients=initial_recipients,
        ),
    )

    message.refresh_from_db()
    assert message.state == MessageState.ACTIVE

    # One email per matching recipient - no co-recipient leakage, and the two
    # non-matching involvements (wrong category, inactive) got nothing.
    assert len(mail.outbox) == 3
    sent_by_email = {sent.to[0]: sent for sent in mail.outbox}
    assert set(sent_by_email) == {offerer.name_and_email, host.name_and_email, injected.name_and_email}

    for sent in mail.outbox:
        assert len(sent.to) == 1
        assert sent.from_email == meta.cloaked_contact_email
        assert sent.reply_to == [meta.plain_contact_email]

    injected_email = sent_by_email[injected.name_and_email]
    html_body = next(content for content, mimetype in injected_email.alternatives if mimetype == "text/html")
    assert isinstance(html_body, str)

    # The author's own Markdown formatting is rendered ...
    assert "<strong>Welcome</strong>" in html_body
    assert "<h1>Important</h1>" in html_body
    # ... but the placeholder value (fully attacker-controlled) is never interpreted as
    # Markdown or HTML, even though it looks exactly like an injection payload.
    assert "<img" not in html_body
    assert "&lt;img" in html_body
    assert 'href="javascript:' not in html_body
    assert "javascript:alert(1)" in html_body  # present, but as inert visible text
    assert "**bold**" in html_body  # the payload's own "markdown" was not parsed
    assert "# heading" in html_body  # nor was its "heading"

    # MessageBody dedup: offerer and host rendered identically; injected differs.
    offerer_recipient = MessageRecipient.objects.get(message=message, person=offerer)
    host_recipient = MessageRecipient.objects.get(message=message, person=host)
    injected_recipient = MessageRecipient.objects.get(message=message, person=injected)
    assert offerer_recipient.body_id == host_recipient.body_id
    assert injected_recipient.body_id != offerer_recipient.body_id

    assert not MessageRecipient.objects.filter(message=message, person=wrong_category_host).exists()
    assert not MessageRecipient.objects.filter(message=message, person=inactive_host).exists()

    # Visible in the recipient's own profile.
    profile_messages = list(OwnProfileType.resolve_messages(offerer, None))
    assert len(profile_messages) == 1
    assert profile_messages[0].subject == "Hello Ada"

    created_entry = Entry.objects.get(entry_type="messages_v2.message.created")
    assert created_entry.other_fields["message_id"] == str(message.id)

    sent_entry = Entry.objects.get(entry_type="messages_v2.message.sent")
    assert sent_entry.other_fields["initial_recipients"] == 3
    assert not any("@" in str(value) for value in sent_entry.other_fields.values())


@pytest.mark.django_db
def test_auto_send_and_non_retroactive_edit():
    event, meta = _setup_event("Messages V2 Auto Send Test")
    universe = event.involvement_universe
    registry = meta.default_registry

    message = Message.objects.create(
        universe=universe,
        subject="Original subject for {FIRST_NAME}",
        body="Original body.",
        dispatch=MessageDispatch.PER_PERSON,
        recipient_filters=[
            [{"dimension": "type", "values": ["program-host"]}, {"dimension": "state", "values": ["active"]}],
        ],
    )
    message.clean_recipient_filters()
    message.sent_at = now()
    message.save()
    assert message.state == MessageState.ACTIVE

    matching_person = Person.objects.create(first_name="Dana", surname="Match", email="dana@example.com")
    matching_involvement = _make_involvement(
        universe, matching_person, registry, type=InvolvementType.PROGRAM_HOST, is_active=True
    )
    matching_involvement.refresh_dependents()

    assert MessageRecipient.objects.filter(message=message, person=matching_person).count() == 1
    assert len(mail.outbox) == 1
    first_recipient = MessageRecipient.objects.get(message=message, person=matching_person)
    assert first_recipient.subject == "Original subject for Dana"
    original_body_id = first_recipient.body_id

    non_matching_person = Person.objects.create(first_name="Eli", surname="NoMatch", email="eli@example.com")
    non_matching_involvement = _make_involvement(
        universe, non_matching_person, registry, type=InvolvementType.PROGRAM_OFFER, is_active=True
    )
    non_matching_involvement.refresh_dependents()

    assert not MessageRecipient.objects.filter(message=message, person=non_matching_person).exists()
    assert len(mail.outbox) == 1

    # Touching an involvement that has already been sent to must not resend/duplicate.
    matching_involvement.title = "updated title, no dimension change"
    matching_involvement.save()
    matching_involvement.refresh_dependents()

    assert MessageRecipient.objects.filter(message=message, person=matching_person).count() == 1
    assert len(mail.outbox) == 1

    # Editing the active message is not retroactive.
    message.subject = "Updated subject for {FIRST_NAME}"
    message.body = "Updated body."
    message.save()

    new_person = Person.objects.create(first_name="Farah", surname="New", email="farah@example.com")
    new_involvement = _make_involvement(
        universe, new_person, registry, type=InvolvementType.PROGRAM_HOST, is_active=True
    )
    new_involvement.refresh_dependents()

    assert len(mail.outbox) == 2
    new_recipient = MessageRecipient.objects.get(message=message, person=new_person)
    assert new_recipient.subject == "Updated subject for Farah"

    # The original recipient's rendered snapshot is unaffected by the edit.
    first_recipient.refresh_from_db()
    assert first_recipient.subject == "Original subject for Dana"
    assert first_recipient.body_id == original_body_id
