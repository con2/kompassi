from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hitpoint2015', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupextra',
            name='night_work',
            field=models.CharField(default='ei', max_length=5, verbose_name='Voitko ty\xf6skennell\xe4 y\xf6ll\xe4?', choices=[('miel', 'Ty\xf6skentelen mielell\xe4ni y\xf6vuorossa'), ('tarv', 'Voin tarvittaessa ty\xf6skennell\xe4 y\xf6vuorossa'), ('ei', 'En vaan voi ty\xf6skennell\xe4 y\xf6vuorossa')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signupextra',
            name='shift_wishes',
            field=models.TextField(help_text='Jos tied\xe4t nyt jo, ettet p\xe4\xe4se paikalle johonkin tiettyyn aikaan tai haluat osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siit\xe4 t\xe4ss\xe4.', verbose_name='Alustavat ty\xf6vuorotoiveet', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='signupextra',
            name='construction',
            field=models.BooleanField(default=False, help_text='Huomaathan, ett\xe4 perjantain ja lauantain v\xe4liselle y\xf6lle ei ole tarjolla majoitusta.', verbose_name='Voin ty\xf6skennell\xe4 jo perjantaina 27. marraskuuta'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='signupextra',
            name='lodging_needs',
            field=models.ManyToManyField(help_text='Ruksaa ne y\xf6t, joille tarvitset lattiamajoitusta. Lattiamajoitus sijaitsee tapahtumapaikalla.', to='hitpoint2015.Night', verbose_name='Tarvitsen lattiamajoitusta', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='signupextra',
            name='total_work',
            field=models.CharField(help_text='Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana? Useimmissa teht\xe4vist\xe4 minimi on kahdeksan tuntia, mutta joissain teht\xe4viss\xe4 se voi olla my\xf6s v\xe4hemm\xe4n (esim. majoitusvalvonta 6 h).', max_length=15, verbose_name='Toivottu kokonaisty\xf6m\xe4\xe4r\xe4', choices=[('8h', 'Minimi - 8 tuntia (1 l\xc3\xa4mmin ateria)'), ('12h', '10\xe2\x80\x9312 tuntia (2 l\xc3\xa4mmint\xc3\xa4 ateriaa)'), ('yli12h', 'Ty\xc3\xb6n Sankari! Yli 12 tuntia! (2 l\xc3\xa4mmint\xc3\xa4 ateriaa)')]),
            preserve_default=True,
        ),
    ]
