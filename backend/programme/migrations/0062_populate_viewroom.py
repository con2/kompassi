from django.db import migrations


def populate_view_room(apps, schema_editor):
    View = apps.get_model("programme", "View")
    ViewRoom = apps.get_model("programme", "ViewRoom")

    for view in View.objects.all():
        for room in view.rooms.all():
            ViewRoom.objects.get_or_create(
                view=view,
                room=room,
                defaults=dict(
                    order=room.order,
                ),
            )


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0061_auto_20171125_1229"),
    ]

    operations = [
        migrations.RunPython(populate_view_room),
    ]
