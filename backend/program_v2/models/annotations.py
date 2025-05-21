from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AnnotationDataType(Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"


class AnnotationSchemoid(BaseModel):
    slug: str
    title: dict[str, str]
    description: dict[str, str] = Field(default_factory=dict)
    type: AnnotationDataType = AnnotationDataType.STRING
    is_public: bool = True
    is_shown_in_detail: bool = True
    is_computed: bool = False

    def validate(self, value: Any):
        """
        Raises ValueError if the value is not valid for the annotation type.
        """
        if self.type == AnnotationDataType.STRING and not isinstance(value, str):
            raise ValueError(f"Value for {self.slug} must be a string.")
        if self.type == AnnotationDataType.NUMBER and not isinstance(value, (int, float)):
            raise ValueError(f"Value for {self.slug} must be a number.")
        if self.type == AnnotationDataType.BOOLEAN and not isinstance(value, bool):
            raise ValueError(f"Value for {self.slug} must be a boolean.")


class ProgramAnnotation(BaseModel):
    annotation: AnnotationSchemoid
    value: Any


# Before putting these into database (and as long as v1 import is a thing), we define them here in the code
ANNOTATIONS = [
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
        slug="konsti:isPlaceholder",
        type=AnnotationDataType.BOOLEAN,
        is_shown_in_detail=False,
        title=dict(
            fi="Näytetään Konstissa ilman ilmoittautumista",
            en="Shown in Konsti without signup",
            sv="Visas i Konsti utan anmälan",
        ),
        description=dict(
            en=(
                "If set, the program item will be shown in Konsti without signup. "
                "This is useful to communicate to visitors that are looking for "
                "programs of a type that often uses Konsti signup that "
                "this program exists but does not require signup."
            ),
        ),
    ),
    AnnotationSchemoid(
        slug="ropecon:numCharacters",
        title=dict(
            fi="Hahmojen määrä",
            en="Number of characters",
            sv="Antal karaktärer",
        ),
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
    AnnotationSchemoid(
        slug="ropecon:isRevolvingDoor",
        type=AnnotationDataType.BOOLEAN,
        title=dict(
            fi="Pyöröoviohjelma",
            en="Hop in, hop out",
        ),
        description=dict(
            fi="Ohjelmanumeroon voi tulla ja lähteä kesken.",
            en="Participants can join and leave the program item while it is running.",
            sv="Deltagare kan gå med i och lämna programmet medan det pågår.",
        ),
    ),
    AnnotationSchemoid(
        slug="internal:formattedHosts",
        title=dict(
            fi="Ohjelmanpitäjät",
            en="Hosts",
            sv="Programvärdar",
        ),
        is_public=False,
        is_shown_in_detail=False,
        is_computed=True,
    ),
    AnnotationSchemoid(
        slug="internal:defaultFormattedHosts",
        title=dict(
            fi="Ohjelmanpitäjäin oletusesitystapa",
            en="Default way to present program hosts",
        ),
        is_public=False,
        is_shown_in_detail=False,
        is_computed=True,
    ),
    AnnotationSchemoid(
        slug="internal:overrideFormattedHosts",
        title=dict(
            fi="Ylikirjoita ohjelmanpitäjäin esitystapa",
            en="Override the way program hosts are presented",
        ),
        description=dict(
            fi="Jos ohjelmanpitäjäin oletusesitystapa ei miellytä, voit ylikirjoittaa sen tässä. Jos jätät tämän tyhjäksi, käytetään oletusesitystapaa.",
            en="If the default way to present program hosts is not to your liking, you can override it here. If you leave this empty, the default formatting will be used.",
        ),
        is_public=False,
        is_shown_in_detail=False,
    ),
    AnnotationSchemoid(
        slug="internal:links:signup",
        title=dict(
            fi="Ilmoittautumislinkki",
            en="Signup link",
            sv="Anmälningslänk",
        ),
        is_public=False,
        is_shown_in_detail=False,
    ),
    AnnotationSchemoid(
        slug="internal:links:tickets",
        title=dict(
            fi="Lipunmyyntilinkki",
            en="Ticket sales link",
            sv="Biljettförsäljningslänk",
        ),
        is_public=False,
        is_shown_in_detail=False,
    ),
    AnnotationSchemoid(
        slug="internal:links:recording",
        title=dict(
            fi="Nauhoitelinkki",
            en="Recording link",
            sv="Inspelningslänk",
        ),
        is_public=False,
        is_shown_in_detail=False,
    ),
    AnnotationSchemoid(
        slug="knutepunkt:tagline",
        title=dict(
            fi="Tagline",
            en="Tag line",
            sv="Tagline",
        ),
    ),
]

ANNOTATIONS_BY_SLUG = {annotation.slug: annotation for annotation in ANNOTATIONS}


def validate_annotations(annotations: dict[str, Any]) -> None:
    """
    Validate the given annotations against the known annotations.

    Args:
        annotations: A dictionary of annotations to validate.
        annotations_list: A list of AnnotationSchemoid objects to validate against.

    Raises:
        ValueError: If any annotation is not valid.
    """
    for slug, value in annotations.items():
        schemoid = ANNOTATIONS_BY_SLUG.get(slug)
        if schemoid is None:
            raise ValueError(f"Unknown annotation slug: {slug}")
        schemoid.validate(value)


def extract_annotations(values: dict[str, Any], annotations=ANNOTATIONS) -> dict[str, Any]:
    """
    Extract known annotations from processed form data.

    Args:
        values: A dictionary of values to extract annotations from.
        annotations: A list of AnnotationSchemoid objects to use for extraction.

    Returns:
        A dictionary containing the extracted annotations.
    """
    annotations = {ann.slug: value for ann in annotations if (value := values.get(ann.slug)) is not None}
    validate_annotations(annotations)
    return annotations
