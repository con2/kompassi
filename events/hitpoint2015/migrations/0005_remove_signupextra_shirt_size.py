from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hitpoint2015", "0004_auto_20150930_2252"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="signupextra",
            name="shirt_size",
        ),
    ]
