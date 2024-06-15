# v1 to v2 importer creates these default dimensions
DATE_DIMENSION_TITLE_LOCALIZED = dict(
    fi="Päivä",
    en="Day",
    sv="Dag",
)

TAG_DIMENSION_TITLE_LOCALIZED = dict(
    fi="Tägit",
    en="Tags",
    sv="Taggar",
)

CATEGORY_DIMENSION_TITLE_LOCALIZED = dict(
    fi="Kategoria",
    en="Category",
    sv="Kategori",
)

ROOM_DIMENSION_TITLE_LOCALIZED = dict(
    fi="Sali",
    en="Room",
    sv="Sal",
)

WEEKDAYS_LOCALIZED = dict(
    fi=["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"],
    en=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    sv=["måndag", "tisdag", "onsdag", "torsdag", "fredag", "lördag", "söndag"],
)


DEFAULT_COLORS = dict(
    color1="#5eb95e",
    color2="#8058a5",
    color3="#0e90d2",
    color4="#dd514c",
    color5="#f37b1d",
    color6="#ff50b8",
    color7="#298da6",
    # these correspond to color1–5
    muu="#5eb95e",
    rope="#8058a5",
    anime="#0e90d2",
    cosplay="#dd514c",
    miitti="#f37b1d",
    # this used to be striped background but let's make it gray
    sisainen="#999999",
)


ANNOTATION_TITLES = {
    "ropecon:contentWarnings": dict(
        fi="Sisältövaroitukset",
        en="Content warnings",
        sv="Innehållsvarningar",
    ),
    "ropecon:accessibilityOther": dict(
        fi="Muut saavutettavuustiedot",
        en="Other accessibility information",
        sv="Övrig tillgänglighetsinformation",
    ),
}
