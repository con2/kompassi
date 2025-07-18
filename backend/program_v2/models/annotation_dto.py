from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from core.utils.text_utils import normalize_whitespace

from .annotation import Annotation
from .enums import AnnotationDataType


class AnnotationDTO(BaseModel, populate_by_name=True):
    slug: str
    title: dict[str, str]
    description: dict[str, str] = Field(default_factory=dict)
    type: AnnotationDataType = Field(default=AnnotationDataType.STRING)

    is_applicable_to_program_items: bool = True
    is_applicable_to_schedule_items: bool = False

    is_public: bool = True
    is_shown_in_detail: bool = True
    is_computed: bool = False

    def to_django(self) -> Annotation:
        return Annotation(
            slug=self.slug,
            title=self.title,
            description=self.description,
            type_slug=self.type.value,
            is_applicable_to_program_items=self.is_applicable_to_program_items,
            is_applicable_to_schedule_items=self.is_applicable_to_schedule_items,
            is_public=self.is_public,
            is_shown_in_detail=self.is_shown_in_detail,
            is_computed=self.is_computed,
        )

    def save(self) -> Annotation:
        return self.save_many([self])[0]

    @classmethod
    def save_many(cls, annotations: list[AnnotationDTO]) -> list[Annotation]:
        update_fields = set(cls.model_fields.keys()) - {"slug", "type"}
        update_fields |= {"type_slug"}

        return Annotation.objects.bulk_create(
            [dto.to_django() for dto in annotations],
            unique_fields=["slug"],
            update_fields=update_fields,
            update_conflicts=True,
        )


class ProgramAnnotation(BaseModel):
    annotation: AnnotationDTO
    value: Any


# Before putting these into database (and as long as v1 import is a thing), we define them here in the code
ANNOTATIONS = [
    AnnotationDTO(
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
    AnnotationDTO(
        slug="konsti:rpgSystem",
        title=dict(
            fi="Pelisysteemi",
            en="RPG system",
            sv="Rollspelssystem",
        ),
    ),
    AnnotationDTO(
        slug="ropecon:otherAuthor",
        title=dict(
            fi="Pelin kirjoittaja (jos muu kuin pelinjohtaja)",
            en="Author (if other than GM)",
            sv="Författare (om annan än spelledaren)",
        ),
    ),
    AnnotationDTO(
        slug="konsti:minAttendance",
        title=dict(
            fi="Minimiosallistujamäärä",
            en="Minimum attendance",
            sv="Minsta antal deltagare",
        ),
        type=AnnotationDataType.NUMBER,
    ),
    AnnotationDTO(
        slug="konsti:maxAttendance",
        title=dict(
            fi="Maksimiosallistujamäärä",
            en="Maximum attendance",
            sv="Högsta antal deltagare",
        ),
        type=AnnotationDataType.NUMBER,
    ),
    AnnotationDTO(
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
            fi=(
                "Jos tämä on valittuna ohjelmanumerolle, se näytetään Konstissa siten, "
                "että siihen ei voi ilmoittautua. Tämä on hyödyllistä, jos haluat viestiä "
                "vieraille, että tällainen ohjelma on olemassa, mutta siihen ei tarvitse ilmoittautua tai "
                "ilmoittautuminen on hoidettu jotain muuta kautta."
            ),
        ),
    ),
    AnnotationDTO(
        slug="ropecon:numCharacters",
        title=dict(
            fi="Hahmojen määrä",
            en="Number of characters",
            sv="Antal karaktärer",
        ),
    ),
    AnnotationDTO(
        slug="konsti:workshopFee",
        title=dict(
            fi="Työpajamaksu",
            en="Workshop fee",
            sv="Workshopavgift",
        ),
    ),
    AnnotationDTO(
        slug="ropecon:contentWarnings",
        title=dict(
            fi="Sisältövaroitukset",
            en="Content warnings",
            sv="Innehållsvarningar",
        ),
    ),
    AnnotationDTO(
        slug="ropecon:accessibilityOther",
        title=dict(
            fi="Muut saavutettavuustiedot",
            en="Other accessibility information",
            sv="Övrig tillgänglighetsinformation",
        ),
    ),
    AnnotationDTO(
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
    AnnotationDTO(
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
    AnnotationDTO(
        slug="internal:defaultFormattedHosts",
        title=dict(
            fi="Ohjelmanpitäjäin oletusesitystapa",
            en="Default way to present program hosts",
        ),
        is_public=False,
        is_shown_in_detail=False,
        is_computed=True,
    ),
    AnnotationDTO(
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
    AnnotationDTO(
        slug="internal:links:signup",
        title=dict(
            fi="Ilmoittautumislinkki",
            en="Signup link",
            sv="Anmälningslänk",
        ),
        is_public=False,
        is_shown_in_detail=False,
    ),
    AnnotationDTO(
        slug="internal:links:tickets",
        title=dict(
            fi="Lipunmyyntilinkki",
            en="Ticket sales link",
            sv="Biljettförsäljningslänk",
        ),
        is_public=False,
        is_shown_in_detail=False,
    ),
    AnnotationDTO(
        slug="internal:links:recording",
        title=dict(
            fi="Nauhoitelinkki",
            en="Recording link",
            sv="Inspelningslänk",
        ),
        is_public=False,
        is_shown_in_detail=False,
    ),
    AnnotationDTO(
        slug="internal:freeformLocation",
        title=dict(
            fi="Vapaamuotoinen sijainti",
            en="Freeform location",
        ),
        description=dict(
            en=normalize_whitespace(
                """
                There are three ways to specify the location of a program item:
                using a room dimension, using a freeform location (this annotation),
                or a combination of both. When both are used, the freeform location
                is appended to the room dimension value in parentheses, eg.
                Main hall (Stage).
                """
            ),
            fi=normalize_whitespace(
                """
                Ohjelmanumeron sijainti voidaan määrittää kolmella tavalla:
                käyttäen salidimensiota, vapaamuotoista sijaintia tai näiden yhdistelmää.
                Molempia käytettäessä vapaamuotoinen sijainti liitetään salidimension
                arvon otsikkoon suluissa, esim. Pääsali (Lava).
                """
            ),
        ),
        is_applicable_to_program_items=False,
        is_applicable_to_schedule_items=True,
        is_public=True,
        is_shown_in_detail=False,  # use location instead
    ),
    AnnotationDTO(
        slug="internal:subtitle",
        title=dict(
            fi="Alaotsikko",
            en="Subtitle",
            sv="Underrubrik",
        ),
        is_applicable_to_program_items=False,
        is_applicable_to_schedule_items=True,
        is_public=True,
        is_shown_in_detail=False,  # use title instead
    ),
]
