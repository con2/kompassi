# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animecon2015', '0007_auto_20150309_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='total_work',
            field=models.CharField(help_text='Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana?', max_length=15, verbose_name='Toivottu kokonaisty\xf6m\xe4\xe4r\xe4', choices=[('minimi', 'Haluan tehd\xe4 vain minimity\xf6panoksen (JV: 10h, muut: 8h)'), ('ekstra', 'Olen valmis tekem\xe4\xe4n lis\xe4tunteja')]),
            preserve_default=True,
        ),
    ]
