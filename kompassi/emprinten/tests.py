import datetime

import pytest

from .functions import fi_bank_barcode


@pytest.mark.parametrize(
    ("iban", "euro", "cents", "viite", "era", "expect"),
    [
        # Test barcode content from "Pankkiviivakoodi-Opas", "Versio 5.3" by "Finanssiala"
        # Lasku 1
        (
            "FI79 4405 2020 0360 82",
            4883,
            15,
            "86851 62596 19897",
            "12.6.2010",
            "479440520200360820048831500000000868516259619897100612",
        ),
        # Lasku 3
        (
            "FI02 5000 4640 0013 02",
            693,
            80,
            "69 87567 20834 35364",
            "24.7.2011",
            "402500046400013020006938000000069875672083435364110724",
        ),
        # Lasku 5, ei eräpäivää
        (
            "FI16 8000 1400 0502 67",
            935,
            85,
            "78 77767 96566 28687",
            None,
            "416800014000502670009358500000078777679656628687000000",
        ),
        # Lasku 6, ei summaa
        (
            "FI73 3131 3001 0000 58",
            0,
            00,
            "8 68624",
            "9.8.2013",
            "473313130010000580000000000000000000000000868624130809",
        ),
        # Lasku 7, max
        (
            "FI83 3301 0001 1007 75",
            150000,
            20,
            "92125 37425 25398 97737",
            "25.5.2016",
            "483330100011007751500002000092125374252539897737160525",
        ),
        # Lasku 9, tulevaisuus
        (
            "FI92 3939 0001 0033 91",
            0,
            2,
            "13 57914",
            "24.12.2099",
            "492393900010033910000000200000000000000001357914991224",
        ),
    ],
)
def test_fi_bank_barcode(iban: str, euro: int, cents: int, viite: str | int, era: str | None, expect: str) -> None:
    _era = datetime.datetime.strptime(era, "%d.%m.%Y").date() if era else None

    result = fi_bank_barcode(iban, euro, cents, viite, _era)
    assert result.valid
    assert result.number == expect


@pytest.mark.parametrize(
    ("iban", "euro", "cents", "viite", "era"),
    [
        # Wrong iban length
        ("FI12 3456 7890 123", 1, 1, "13 57914", None),
        # Wrong prefix
        ("SE12 3456 7890 12", 1, 1, "13 57914", None),
        # Invalid cents
        ("FI12 3456 7890 12", 1, 100, "13 57914", None),
        # Invalid cents
        ("FI12 3456 7890 12", 1, -1, "13 57914", None),
        # Invalid euros
        ("FI12 3456 7890 12", 1_000_000, 0, "13 57914", None),
        # Invalid euros
        ("FI12 3456 7890 12", -1, 0, "13 57914", None),
        # Requires V5 barcode which is not supported
        ("FI12 3456 7890 12", 1, 0, "RF61 6987 5672 0839", None),
    ],
)
def test_fi_bank_barcode_invalid(iban: str, euro: int, cents: int, viite: str | int, era: str | None) -> None:
    _era = datetime.datetime.strptime(era, "%d.%m.%Y").date() if era else None

    result = fi_bank_barcode(iban, euro, cents, viite, _era)
    assert not result.valid
