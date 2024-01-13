from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0002_grantedprivilege_state"),
    ]

    operations = [
        migrations.CreateModel(
            name="SlackAccess",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("team_name", models.CharField(max_length=255)),
                ("api_token", models.CharField(default="test", max_length=255)),
                (
                    "privilege",
                    models.OneToOneField(on_delete=models.CASCADE, related_name="slack_access", to="access.Privilege"),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
