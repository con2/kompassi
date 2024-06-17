# v1 to v2 importer creates these default dimensions
from .models.annotations import AnnotationDataType, AnnotationSchemoid

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


ANNOTATION_SCHEMA = [
    AnnotationSchemoid(
        slug="ropecon:gameSlogan",
        title=dict(
            fi="Pelin slogan",
            en="Game slogan",
            sv="Spelets slogan",
        ),
        description=dict(
            fi="Lyhyt lause, joka kertoo pelaajille mitä peli tarjoaa. Esimerkiksi ”Perinteinen D&D-luolaseikkailu”, tai ”Lovecraftilaista kauhua Equestriassa”.",
            en='One short sentence that will let players know what the game has to offer. For example, "A traditional D&D dungeon crawl", or "Lovecraftian horror in Equestria".',
            sv="En kort mening som berättar för spelarna vad spelet erbjuder. Till exempel ”En traditionell D&D-dungeon crawl” eller ”Lovecraftsk skräck i Equestria”.",
        ),
    ),
    AnnotationSchemoid(
        slug="konsti:rpgSystem",
        title=dict(
            fi="Pelisysteemi",
            en="RPG system",
            sv="Rollspelssystem",
        ),
    ),
    AnnotationSchemoid(
        slug="ropecon:otherAuthor",
        title=dict(
            fi="Pelin kirjoittaja (jos muu kuin pelinjohtaja)",
            en="Author (if other than GM)",
            sv="Författare (om annan än spelledaren)",
        ),
    ),
    AnnotationSchemoid(
        slug="konsti:minAttendance",
        title=dict(
            fi="Minimiosallistujamäärä",
            en="Minimum attendance",
            sv="Minsta antal deltagare",
        ),
        type=AnnotationDataType.NUMBER,
    ),
    AnnotationSchemoid(
        slug="konsti:maxAttendance",
        title=dict(
            fi="Maksimiosallistujamäärä",
            en="Maximum attendance",
            sv="Högsta antal deltagare",
        ),
        type=AnnotationDataType.NUMBER,
    ),
    AnnotationSchemoid(
        slug="ropecon:numCharacters",
        title=dict(
            fi="Hahmojen määrä",
            en="Number of characters",
            sv="Antal karaktärer",
        ),
        type=AnnotationDataType.NUMBER,
    ),
    AnnotationSchemoid(
        slug="konsti:workshopFee",
        title=dict(
            fi="Työpajamaksu",
            en="Workshop fee",
            sv="Workshopavgift",
        ),
    ),
    AnnotationSchemoid(
        slug="ropecon:contentWarnings",
        title=dict(
            fi="Sisältövaroitukset",
            en="Content warnings",
            sv="Innehållsvarningar",
        ),
    ),
    AnnotationSchemoid(
        slug="ropecon:accessibilityOther",
        title=dict(
            fi="Muut saavutettavuustiedot",
            en="Other accessibility information",
            sv="Övrig tillgänglighetsinformation",
        ),
    ),
]
