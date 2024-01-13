from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("test", models.IntegerField(null=True, blank=True)),
                ("VERSION", models.CharField(max_length=4)),
                ("STAMP", models.CharField(max_length=20)),
                ("REFERENCE", models.CharField(max_length=20)),
                ("PAYMENT", models.CharField(max_length=20)),
                ("STATUS", models.IntegerField()),
                ("ALGORITHM", models.IntegerField()),
                ("MAC", models.CharField(max_length=32)),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
