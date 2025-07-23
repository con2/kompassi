"""
At Solmukohta 2024, the participants are requested to fill in a Google form for providing
details not gathered during the ticket purchase process.

This script checks that the people who have signed up have a ticket and that the ticket holders
have signed up.

Extra dependencies need to be installed for this to work:

    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

Google API credentials need to be obtained and stored in the working directory as credentials.json.
The first time this script is run, it will open a browser window for authentication and store the
token in token.json. In order for this to work, you may need to run it outside Docker Compose:

    POSTGRES_HOSTNAME=localhost python manage.py solmukohta2024_ticket_control
"""

import os.path
import re
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import cache

from django.core.management.base import BaseCommand
from tabulate import tabulate

from kompassi.zombies.tickets.models import Order

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# TODO: FILL IN! The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1WCF0J7Aw0Hzd-rU9txQKnyzGIK4nF85sLvKm1YM1TyY"
ORDER_NUMBER_RANGE = "DO NOT EDIT!C:C"

# Forward results will be stored in a column on the same sheet as original responses.
FORWARD_RESULTS_ANCHOR = "DO NOT EDIT!X2"

# Reverse results will be stored on a sheet of their own.
REVERSE_RESULTS_ANCHOR = "Ticket control reverse results!A1"

EVENT_SLUG = "solmukohta2024"


class Result(Enum):
    UNKNOWN = "UNKNOWN"
    OK = "OK"
    NO_SUCH_ORDER = "NO_SUCH_ORDER"
    ORDER_NOT_PAID = "ORDER_NOT_PAID"
    ORDER_CANCELLED = "ORDER_CANCELLED"
    TOO_MANY_SIGNUPS = "TOO_MANY_SIGNUPS"
    TOO_FEW_SIGNUPS = "TOO_FEW_SIGNUPS"


@cache
def get_credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def clean_up_order_number(order_number: str):
    return int(re.sub(r"\D", "", order_number))


def format_order_number(order_number: int):
    return f"#{order_number:06d}"


def get_order_numbers(spreadsheet_id=SPREADSHEET_ID, range=ORDER_NUMBER_RANGE):
    from googleapiclient.discovery import build

    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range).execute()

    # omit header row and clean up data
    return [clean_up_order_number(row[0]) for row in result["values"][1:]]


def get_number_of_tickets(order: Order):
    num_tickets = 0

    for op in order.order_product_set.all():
        if "Single person" in op.product.name:
            continue
        elif "Suite" in op.product.name or "Business" in op.product.name:
            num_tickets += 2 * op.count
        else:
            num_tickets += op.count

    return num_tickets


def check_order(order: Order, num_signups_by_order_number: Counter):
    num_signups = num_signups_by_order_number[order.id]
    num_tickets = get_number_of_tickets(order)

    if order.confirm_time is None or order.payment_date is None:
        return Result.ORDER_NOT_PAID
    elif order.cancellation_time is not None:
        return Result.ORDER_CANCELLED
    elif num_signups > num_tickets:
        return Result.TOO_MANY_SIGNUPS
    elif num_signups < num_tickets:
        return Result.TOO_FEW_SIGNUPS
    else:
        return Result.OK


def forward_check(order_numbers: list[int], num_signups_by_order_number: Counter):
    """
    Ensure signed up people have a ticket
    """
    forward_results: list[tuple[int, str]] = []

    for order_number in order_numbers:
        result = Result.UNKNOWN

        try:
            order = Order.objects.get(event__slug=EVENT_SLUG, id=order_number)
        except Order.DoesNotExist:
            result = Result.NO_SUCH_ORDER
        else:
            result = check_order(order, num_signups_by_order_number)

        forward_results.append((order_number, result.value))

    return forward_results


def write_forward_results(forward_results: list[tuple[int, str]]):
    from googleapiclient.discovery import build

    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()

    # Write forward results to the same sheet as the original responses
    body = {"values": forward_results}
    result = (
        sheet.values()
        .update(
            spreadsheetId=SPREADSHEET_ID,
            range=FORWARD_RESULTS_ANCHOR,
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )
    print(f"Wrote forward results ({result.get('updatedCells')} cells updated)")


@dataclass
class ReverseCheckResult:
    order_number: int
    email: str
    result: Result

    HEADER_ROW = ["Order number", "Email", "Result"]

    def as_row(self):
        return [format_order_number(self.order_number), self.email, self.result.value]


def reverse_check(num_signups_by_order_number: Counter):
    """
    Ensure ticket holders have signed up
    """
    reverse_results = []

    for order in Order.objects.filter(
        event__slug=EVENT_SLUG,
        confirm_time__isnull=False,
        payment_date__isnull=False,
        cancellation_time__isnull=True,
    ):
        assert order.customer
        result = check_order(order, num_signups_by_order_number)
        reverse_results.append(ReverseCheckResult(order.id, order.customer.email, result))

    return reverse_results


def write_reverse_results(reverse_results: list[ReverseCheckResult]):
    from googleapiclient.discovery import build

    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()

    # Write reverse results to their dedicated sheet (must exist already)
    body = {"values": [ReverseCheckResult.HEADER_ROW] + [result.as_row() for result in reverse_results]}
    result = (
        sheet.values()
        .update(
            spreadsheetId=SPREADSHEET_ID,
            range=REVERSE_RESULTS_ANCHOR,
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )
    print(f"Wrote reverse results ({result.get('updatedCells')} cells updated)")


class Command(BaseCommand):
    help = "Ensure signed up people have a ticket and ticket holders have signed up"

    def add_arguments(self, parser):
        parser.add_argument(
            "--really",
            help="Write out results to the Google sheet",
            default=False,
            action="store_true",
        )

    def handle(self, *args, **options):
        order_numbers = get_order_numbers()
        num_signups_by_order_number = Counter(order_numbers)

        forward_results = forward_check(order_numbers, num_signups_by_order_number)
        print(tabulate(forward_results, headers=["Order number", "Result"]))
        print()

        forward_results_summary = Counter(result for (_, result) in forward_results)
        print(tabulate(forward_results_summary.items(), headers=["Result", "Count"]))
        print()

        reverse_results = reverse_check(num_signups_by_order_number)
        print(
            tabulate(
                [(result.order_number, result.result.value) for result in reverse_results],
                headers=["Order number", "Result"],
            )
        )
        print()

        reverse_results_summary = Counter(result.result.value for result in reverse_results)
        print(tabulate(reverse_results_summary.items(), headers=["Result", "Count"]))
        print()

        if options["really"]:
            write_forward_results(forward_results)
            write_reverse_results(reverse_results)
        else:
            print("Pass --really to write results to Google Sheets.")
