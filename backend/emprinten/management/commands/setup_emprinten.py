import logging
import pathlib

from django.conf import settings
from django.core.files.base import File
from django.core.management.base import BaseCommand

import core.models
from core.utils import log_get_or_create

from ...models import FileVersion, Project, ProjectFile

logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    args = ""
    help = "Setup emprinten specific stuff"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            print("Not creating example for production")
            return

        # Example for LabourEventMeta.work_certificate_pdf_project:

        project, created = Project.objects.get_or_create(
            slug="example_pdf",
            defaults={
                "name": "Esimerkki työtodistus",
                "split_output": False,
                "name_pattern": "työtodistus {{row.full_name|filename}}",
                "title_pattern": "Työtodistus: {{row.full_name}}",
            },
        )
        log_get_or_create(logger, project, created)

        # Note: Main, instead of HTML (which is meant for includes)
        self._create_file(project, "example.html", ProjectFile.Type.Main)
        self._create_file(project, "example.css", ProjectFile.Type.CSS)
        self._create_file(project, "example.png", ProjectFile.Type.Image)

        # Example for CSV upload via /dummy_event/emp/csv_example/:
        # You may use csv_example.csv from this directory to test the feature out.

        # Make UI accessible on Dummy event by mahti.
        event, created = core.models.Event.get_or_create_dummy()
        log_get_or_create(logger, event, created)

        project, created = Project.objects.get_or_create(
            slug="csv_example",
            defaults={
                "name": "Käsityötodistus",
                "event": event,
                "split_output": True,
                "name_pattern": "työtodistus {{row.full_name|filename}}",
                "title_pattern": "Työtodistus: {{row.full_name}}",
            },
        )
        log_get_or_create(logger, project, created)

        # Note: Main, instead of HTML (which is meant for includes)
        self._create_file(project, "csv_example.html", ProjectFile.Type.Main)
        self._create_file(project, "example.css", ProjectFile.Type.CSS)
        self._create_file(project, "example.png", ProjectFile.Type.Image)

    @staticmethod
    def _create_file(project: Project, file_name: str, file_type: ProjectFile.Type):
        project_file, created = ProjectFile.objects.get_or_create(
            project=project,
            file_name=file_name,
            defaults={
                "type": file_type,
            },
        )
        log_get_or_create(logger, project_file, created)

        versions = FileVersion.objects.filter(file=project_file, current=True)
        if versions:
            file_version = versions[0]
            created = False
        else:
            path = pathlib.Path(__file__).parent / file_name
            if file_type == ProjectFile.Type.Image:
                with path.open(mode="rb") as content:
                    file_version = FileVersion.objects.create(
                        current=True,
                        data=File(content, name=file_name),
                        file=project_file,
                    )
            else:
                with path.open(encoding="utf-8") as content:
                    file_version = FileVersion.objects.create(
                        current=True,
                        data=File(content, name=file_name),
                        file=project_file,
                    )

            created = True
        log_get_or_create(logger, file_version, created)
