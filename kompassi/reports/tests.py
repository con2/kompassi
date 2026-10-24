import io
import zipfile
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from django.utils.timezone import now

from kompassi.access.models.cbac_entry import CBACEntry
from kompassi.core.models.event import Event
from kompassi.core.models.person import Person
from kompassi.event_log_v2.models.entry import Entry
from kompassi.tickets_v2.models.meta import TicketsV2EventMeta

from .export import get_filename, write_csv, write_xlsx
from .models.column import Column
from .models.enums import TypeOfColumn
from .models.report import Report

HELSINKI = ZoneInfo("Europe/Helsinki")


def _hourly_report() -> Report:
    return Report(
        slug="ticket_exchange_by_hour",
        title=dict(en="Exchanged tickets by hour"),
        columns=[
            Column(slug="hour", title=dict(en="Hour"), type=TypeOfColumn.DATETIME),
            Column(slug="arrivals", title=dict(en="Arrivals"), type=TypeOfColumn.INT),
        ],
        rows=[
            ["2025-07-26T12:00:00+03:00", 1],
            ["2025-07-25T10:00:00+03:00", 3],
            ["Not exchanged", 10],
        ],
    )


def _text_report() -> Report:
    return Report(
        slug="ticket_exchange_by_product",
        title=dict(en="Ticket exchange by product"),
        columns=[
            Column(slug="product", title=dict(en="Product"), type=TypeOfColumn.STRING),
            Column(slug="change", title=dict(en="Change"), type=TypeOfColumn.INT),
            Column(slug="price", title=dict(en="Price"), type=TypeOfColumn.CURRENCY),
            Column(slug="share", title=dict(en="Share"), type=TypeOfColumn.PERCENTAGE),
        ],
        rows=[
            ['Weekend ticket, "adult"', -2, "12.50", 0.25],
            ['=HYPERLINK("http://example.com")', 1, None, None],
        ],
    )


def test_filename_from_datetime_column():
    filename = get_filename(_hourly_report(), "ropecon2025", HELSINKI, "csv")
    assert filename == "ropecon2025_ticket_exchange_by_hour_2025-07-25T1000_2025-07-26T1200.csv"


def test_filename_until_export_time():
    exported_at = datetime(2026, 10, 24, 12, 30, tzinfo=UTC)
    filename = get_filename(_text_report(), "ropecon2025", HELSINKI, "xlsx", exported_at)
    assert filename == "ropecon2025_ticket_exchange_by_product_until_2026-10-24T1530.xlsx"


def test_csv():
    buf = io.BytesIO()
    write_csv(_text_report(), "en", buf)
    data = buf.getvalue()

    assert data.startswith(b"\xef\xbb\xbf")
    assert data.decode("utf-8-sig").split("\r\n") == [
        "Product,Change,Price,Share",
        '"Weekend ticket, ""adult""",-2,12.50,0.25',
        # formula neutralized in the text column, while the negative number above keeps its sign
        '"\'=HYPERLINK(""http://example.com"")",1,,',
        "",
    ]


def test_xlsx():
    buf = io.BytesIO()
    write_xlsx(_hourly_report(), "en", HELSINKI, buf)

    with zipfile.ZipFile(buf) as xlsx:
        sheet = xlsx.read("xl/worksheets/sheet1.xml").decode()
        shared_strings = xlsx.read("xl/sharedStrings.xml").decode()
        workbook = xlsx.read("xl/workbook.xml").decode()

    assert 'name="Exchanged tickets by hour"' in workbook
    # 2025-07-26 12:00 local time as an Excel serial date, ie. a real date and not a string
    assert "<v>45864.5</v>" in sheet
    assert "<v>3</v>" in sheet
    assert "Not exchanged" in shared_strings
    assert "+03:00" not in shared_strings


@pytest.fixture
def tickets_event(db):
    event, _ = Event.get_or_create_dummy(name="Report export test event")
    (admin_group,) = TicketsV2EventMeta.get_or_create_groups(event, ["admins"])
    meta, _ = TicketsV2EventMeta.objects.update_or_create(
        event=event,
        defaults=dict(
            admin_group=admin_group,
            contact_email="Test Ticket Sales <tickets@example.com>",
        ),
    )
    meta.ensure_partitions()
    Entry.ensure_partitions()
    return event


@pytest.mark.django_db
def test_event_report_export_requires_access(client, tickets_event: Event):
    url = f"/events/{tickets_event.slug}/tickets/reports/ticket_exchange_by_product.csv"

    def assert_denied():
        # NOTE: permission_denied_view renders the 403 page with status 200
        response = client.get(url)
        assert "Content-Disposition" not in response
        assert response["Content-Type"].startswith("text/html")

    assert_denied()

    person, _ = Person.get_or_create_dummy(superuser=False, another=True)
    client.force_login(person.user)
    assert_denied()

    CBACEntry.objects.create(
        user=person.user,
        claims={"event": tickets_event.slug, "app": "tickets_v2"},
        valid_from=now(),
        valid_until=now() + timedelta(days=1),
    )
    response = client.get(url + "?lang=fi")
    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv; charset=utf-8"
    assert f'filename="{tickets_event.slug}_ticket_exchange_by_product_until_' in response["Content-Disposition"]
    assert response.content.decode("utf-8-sig").startswith("Tuote,")

    response = client.get(url.replace(".csv", ".xlsx"))
    assert response.status_code == 200
    assert response.content.startswith(b"PK")

    assert client.get(url.replace("ticket_exchange_by_product", "no_such_report")).status_code == 404


@pytest.mark.django_db
def test_stats_report_export_is_public(client):
    response = client.get("/stats/reports/kompassi_stats_counts.csv")
    assert response.status_code == 200
    assert 'filename="kompassi_kompassi_stats_counts_until_' in response["Content-Disposition"]


def test_xlsx_number_formats():
    buf = io.BytesIO()
    write_xlsx(_text_report(), "en", HELSINKI, buf)

    with zipfile.ZipFile(buf) as xlsx:
        sheet = xlsx.read("xl/worksheets/sheet1.xml").decode()
        styles = xlsx.read("xl/styles.xml").decode()
        shared_strings = xlsx.read("xl/sharedStrings.xml").decode()

    assert "<v>-2</v>" in sheet
    assert "<v>12.5</v>" in sheet
    assert "<v>0.25</v>" in sheet
    assert 'formatCode="#,##0.00 €"' in styles
    assert 'formatCode="0.0%"' in styles
    # stored as a string, so Excel shows it rather than running it
    assert "<f>" not in sheet
    assert "=HYPERLINK" in shared_strings
