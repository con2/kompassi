from django.db import migrations


def forwards_func(apps, schema_editor):
    Badge = apps.get_model("badges", "Badge")
    Signup = apps.get_model("labour", "Signup")
    PersonnelClass = apps.get_model("labour", "PersonnelClass")

    for signup in Signup.objects.all():
        event = signup.event
        person = signup.person

        try:
            badge = Badge.objects.get(template__event=event, person=person)
        except Badge.DoesNotExist:
            personnel_class, unused = PersonnelClass.objects.get_or_create(
                event=event,
                slug="tyovoima",
                defaults=dict(
                    app_label="labour",
                    name="Työvoima",
                ),
            )
        else:
            personnel_class, unused = PersonnelClass.objects.get_or_create(
                event=event,
                slug=badge.template.slug,
                defaults=dict(
                    app_label="labour",
                    name=badge.template.name,
                ),
            )

        signup.personnel_classes = [personnel_class]
        signup.save()


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0002_auto_20141115_1102"),
        ("badges", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards_func, elidable=True),
    ]
