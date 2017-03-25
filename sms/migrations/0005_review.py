# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0004_vote_has_nominee_not_another_way_round'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotword',
            options={'verbose_name': 'Avainsana', 'verbose_name_plural': 'Avainsanat'},
        ),
        migrations.AlterField(
            model_name='hotword',
            name='hotword',
            field=models.CharField(help_text='T\xe4ll\xe4 nimell\xe4 erotat avainsanan muista, esim. toisen tapahtuman AMV-\xe4\xe4nestyksest\xe4', max_length=255, verbose_name='Avainsanan kuvaus'),
            preserve_default=True,
        ),
    ]
