from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yukicon2016', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='construction',
            field=models.BooleanField(default=False, verbose_name='Voin ty\xf6skennell\xe4 jo perjantaina'),
            preserve_default=True,
        ),
    ]
