from __future__ import annotations

import os
import typing

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from kompassi.core.models import Event


class Project(models.Model):
    name = models.CharField(max_length=255, null=False)
    slug = models.SlugField(unique=True, help_text="Do not change after any file version has been added!")
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="If set, project is accessible on generator UI by CBAC allowlist.",
    )

    split_output = models.BooleanField(
        null=False,
        help_text="If set, produce a zip archive containing one or more PDFs instead of a single PDF.",
    )
    name_pattern = models.CharField(
        max_length=255,
        null=False,
        blank=True,
        help_text="File name template pattern without file extension."
        " Gets row dictionary as context unless rendering multiple rows and Split output is not set.",
    )
    title_pattern = models.CharField(
        max_length=255,
        null=False,
        help_text="PDF title template pattern."
        " Gets row dictionary as context unless rendering multiple rows and Split output is not set.",
    )

    def __str__(self) -> str:
        if self.event is not None:
            return f"{self.event} / {self.slug}: {self.name}"
        else:
            return f"{self.slug}: {self.name}"

    def current_files(self) -> typing.Iterable[FileVersion]:
        return FileVersion.objects.filter(file__project=self, current=True).select_related("file")

    def is_allowed_to_supply_data(self, user: AbstractUser) -> bool:
        if self.event is None:
            return False

        from kompassi.access.models.cbac_entry import CBACEntry

        return CBACEntry.is_allowed(user, self.event.get_claims(app=self._meta.app_label, slug=self.slug))


class ProjectFile(models.Model):
    class Type(models.TextChoices):
        Main = "main"
        HTML = "html"
        CSS = "css"
        CSV = "csv"
        Image = "img"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    file_name = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=4, null=False, choices=Type.choices)

    hidden = models.BooleanField(default=False, null=False)
    editable = models.BooleanField(default=False, null=False)
    transient = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return f"{self.project}/{self.file_name} ({self.type})"

    class Meta:
        unique_together = (("project", "file_name"),)


def make_filename(instance: FileVersion, filename: str) -> str:
    parts = os.path.splitext(os.path.basename(filename))
    if parts[1]:
        name = f"{parts[0]}-{instance.version}{parts[1]}"
    else:
        name = f"{parts[0]}-{instance.version}"
    return os.path.join(
        instance._meta.app_label,
        instance.file.project.slug,
        name,
    )


class FileVersion(models.Model):
    file = models.ForeignKey(ProjectFile, on_delete=models.CASCADE, null=False)
    data = models.FileField(upload_to=make_filename, null=False)
    version = models.PositiveIntegerField(default=1, null=False)
    current = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["file"],
                condition=models.Q(current=True),
                name="unique_current_file",
            ),
        ]
        unique_together = (("file", "version"),)

    def __str__(self) -> str:
        return f"{self.data.name} (v{self.version})"


class RenderResult(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    row_count = models.PositiveIntegerField()
    started = models.DateTimeField(auto_now_add=True)
