from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("membership", "0009_auto_20151011_2236"),
    ]

    operations = [  # noqa: RUF012
        migrations.RemoveField(
            model_name="membershiporganizationmeta",
            name="membership_fee",
        ),
    ]
