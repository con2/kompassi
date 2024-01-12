from django.db import migrations


def populate_badge_personnel_class(apps, schema_editor):
    Badge = apps.get_model("badges", "Badge")
    PersonnelClass = apps.get_model("labour", "PersonnelClass")

    for badge in Badge.objects.all():
        if badge.personnel_class is None and badge.template is not None:
            badge.personnel_class, unused = PersonnelClass.objects.get_or_create(
                event=badge.template.event,
                slug=badge.template.slug,
                defaults=dict(
                    name=badge.template.name,
                    app_label="labour",
                ),
            )
            badge.save()


def populate_batch_personnel_class(apps, schema_editor):
    Batch = apps.get_model("badges", "Batch")
    PersonnelClass = apps.get_model("labour", "PersonnelClass")

    for batch in Batch.objects.all():
        if batch.personnel_class is None and batch.template is not None:
            batch.personnel_class, unused = PersonnelClass.objects.get_or_create(
                event=batch.template.event,
                slug=batch.template.slug,
                defaults=dict(
                    name=batch.template.name,
                    app_label="labour",
                ),
            )
            batch.save()


class Migration(migrations.Migration):
    dependencies = [
        ("badges", "0002_personnel_class"),
    ]

    operations = [
        migrations.RunPython(populate_badge_personnel_class, elidable=True),
        migrations.RunPython(populate_batch_personnel_class, elidable=True),
    ]
