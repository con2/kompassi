# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animecon2015', '0006_auto_20150309_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signupextra',
            name='shift_type',
        ),
        migrations.AlterField(
            model_name='signupextra',
            name='total_work',
            field=models.CharField(help_text='Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana?', max_length=15, verbose_name='Toivottu kokonaisty\xf6m\xe4\xe4r\xe4', choices=[('minimi', 'Haluan tehd\xc3\xa4 vain minimity\xc3\xb6panoksen (JV: 10h, muut: 8h)'), ('ekstra', 'Olen valmis tekem\xc3\xa4\xc3\xa4n lis\xc3\xa4tunteja')]),
        ),
    ]
