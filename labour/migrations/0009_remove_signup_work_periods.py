from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0008_auto_20150419_1438"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="signup",
            name="work_periods",
        ),
    ]
