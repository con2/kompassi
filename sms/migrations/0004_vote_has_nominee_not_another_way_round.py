# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0003_refactoring'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nominee',
            name='vote',
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote',
            field=models.ForeignKey(on_delete=models.CASCADE, to='sms.Nominee'),
            preserve_default=True,
        ),
    ]
