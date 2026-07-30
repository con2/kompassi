from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("core", "0016_person_allow_work_history_sharing"),
    ]

    operations = [  # noqa: RUF012
        migrations.RemoveField(
            model_name="event",
            name="headline",
        ),
    ]
