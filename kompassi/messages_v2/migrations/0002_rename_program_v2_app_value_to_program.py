from django.db import migrations


def rename_program_v2_to_program(apps, schema_editor):
    Message = apps.get_model("messages_v2", "Message")
    MessageReplyTo = apps.get_model("messages_v2", "MessageReplyTo")
    Message.objects.filter(app="program_v2").update(app="program")
    MessageReplyTo.objects.filter(app="program_v2").update(app="program")


def rename_program_to_program_v2(apps, schema_editor):
    Message = apps.get_model("messages_v2", "Message")
    MessageReplyTo = apps.get_model("messages_v2", "MessageReplyTo")
    Message.objects.filter(app="program").update(app="program_v2")
    MessageReplyTo.objects.filter(app="program").update(app="program_v2")


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("messages_v2", "0001_initial"),
    ]

    operations = [  # noqa: RUF012
        # The old MessageApp-derived CheckConstraint only allows "program_v2" - it must
        # be dropped before the data fix below can write "program" into these columns.
        # The replacement DimensionApp-derived constraint is added in the next migration.
        migrations.RemoveConstraint(
            model_name="message",
            name="messages_v2_Message_app_MessageApp",
        ),
        migrations.RemoveConstraint(
            model_name="messagereplyto",
            name="messages_v2_MessageReplyTo_app_MessageApp",
        ),
        migrations.RunPython(
            rename_program_v2_to_program,
            rename_program_to_program_v2,
            elidable=True,
        ),
    ]
