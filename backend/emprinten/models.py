from __future__ import annotations

import os
import typing

from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255, null=False)
    slug = models.SlugField(unique=True, null=False)

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
        return f"{self.slug}: {self.name}"

    def current_files(self) -> typing.Iterable[FileVersion]:
        return FileVersion.objects.filter(file__project=self, current=True).select_related("file")


class ProjectFile(models.Model):
    class Type(models.TextChoices):
        Main = "main"
        HTML = "html"
        CSS = "css"
        CSV = "csv"
        Image = "img"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    file_name = models.CharField(max_length=255, null=False, unique=True)
    type = models.CharField(max_length=4, null=False, choices=Type.choices)

    hidden = models.BooleanField(default=False, null=False)
    editable = models.BooleanField(default=False, null=False)
    transient = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return f"{self.project}/{self.file_name} ({self.type})"


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
