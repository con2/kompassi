from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hitpoint2015', '0005_remove_signupextra_shirt_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='total_work',
            field=models.CharField(help_text='Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana? Useimmissa teht\xe4vist\xe4 minimi on kahdeksan tuntia, mutta joissain teht\xe4viss\xe4 se voi olla my\xf6s v\xe4hemm\xe4n (esim. majoitusvalvonta 6 h).', max_length=15, verbose_name='Toivottu kokonaisty\xf6m\xe4\xe4r\xe4', choices=[('8h', 'Minimi - 8 tuntia'), ('12h', '10\xe2\x80\x9312 tuntia'), ('yli12h', 'Ty\xc3\xb6n Sankari! Yli 12 tuntia!')]),
            preserve_default=True,
        ),
    ]
