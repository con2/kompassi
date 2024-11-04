from pathlib import Path

import yaml
from django.core.management.base import BaseCommand, CommandParser

from core.models.event import Event

from ...models.dimension import DimensionDTO
from ...models.survey import Survey


class Command(BaseCommand):
    help = "Dump a survey to YAML files"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("event_slug", type=str, help="The slug for the event")
        parser.add_argument("survey_slug", type=str, help="The slug for the survey")

    def handle(self, *args, **options):
        event = Event.objects.get(slug=options["event_slug"])
        survey = Survey.objects.get(slug=options["survey_slug"], event=event)

        forms_path = Path("events") / event.slug / "forms"
        forms_path.mkdir(parents=True, exist_ok=True)

        for language in survey.languages.all():
            form_path = forms_path / f"{survey.slug}-{language.language}.yml"
            with form_path.open("w") as output_file:
                yaml.dump(
                    dict(
                        title=language.title,
                        description=language.description,
                        thank_you_message=language.thank_you_message,
                        fields=[{k: v for (k, v) in field.items() if v is not None} for field in language.fields],
                    ),
                    output_file,
                    sort_keys=False,
                    allow_unicode=True,
                )
            self.stdout.write(f"Wrote {form_path}")

        dimensions_path = forms_path / f"{survey.slug}-dimensions.yml"
        with dimensions_path.open("w") as output_file:
            yaml.dump(
                [DimensionDTO.from_model(dimension).model_dump(mode="json") for dimension in survey.dimensions.all()],
                output_file,
                sort_keys=False,
                allow_unicode=True,
            )
        self.stdout.write(f"Wrote {dimensions_path}")
