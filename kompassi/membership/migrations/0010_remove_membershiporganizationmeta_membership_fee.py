from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0009_auto_20151011_2236"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="membershiporganizationmeta",
            name="membership_fee",
        ),
    ]
