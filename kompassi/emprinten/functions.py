from __future__ import annotations

import base64
import datetime
import typing

from .svg_code128 import SvgCode128


def get() -> dict[str, typing.Callable]:
    return {
        "fi_bank_barcode": fi_bank_barcode,
    }


class FiBankBarCode(typing.NamedTuple):
    valid: bool
    number: str
    svg64: str

    @classmethod
    def invalid(cls) -> FiBankBarCode:
        return FiBankBarCode(valid=False, number="", svg64="")


def _number_or_none(number: str | int | None) -> int | None:
    if isinstance(number, str):
        if number.isdigit():
            return int(number)
    elif isinstance(number, int):
        return number
    return None


FI_BANK_IBAN_LENGTH = 16
FI_BANK_MAX_EUROCENTS = 99
FI_BANK_MAX_EUROS = 1_000_000
FI_BANK_MAX_REF_LENGTH = 20
FI_BANK_VIRTUAL_BARCODE_LENGTH = 54


def fi_bank_barcode(iban: str, euro: int, cents: int, viite: str | int, era: datetime.date | None) -> FiBankBarCode:
    _euro = _number_or_none(euro)
    _cents = _number_or_none(cents)
    if iban is None or _euro is None or _cents is None or viite is None:
        return FiBankBarCode.invalid()

    if (
        not iban
        or not iban.startswith("FI")
        or _cents < 0
        or _cents > FI_BANK_MAX_EUROCENTS
        or _euro < 0
        or _euro >= FI_BANK_MAX_EUROS
    ):
        return FiBankBarCode.invalid()

    iban = iban.replace(" ", "").removeprefix("FI")
    if len(iban) != FI_BANK_IBAN_LENGTH or not iban.isdigit():
        return FiBankBarCode.invalid()

    if not isinstance(viite, str):
        viite = str(viite)
    viite = viite.replace(" ", "")
    if len(viite) > FI_BANK_MAX_REF_LENGTH or not viite.isdigit():
        return FiBankBarCode.invalid()

    _era = era.strftime("%y%m%d") if era else "000000"
    vv = f"4{iban}{_euro:06d}{_cents:02d}000{viite:0>20s}{_era}"
    if len(vv) != FI_BANK_VIRTUAL_BARCODE_LENGTH:
        return FiBankBarCode.invalid()

    code = SvgCode128(vv)
    svg = code.draw_svg()
    svg64 = base64.b64encode(svg).decode("utf-8")
    return FiBankBarCode(valid=True, number=vv, svg64=svg64)
