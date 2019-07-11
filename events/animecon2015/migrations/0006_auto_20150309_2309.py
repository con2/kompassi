from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animecon2015', '0005_remove_signupextra_shirt_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='shift_type',
            field=models.CharField(help_text='Haluatko tehd\xe4 yhden pitk\xe4n ty\xf6vuoron vaiko monta lyhyemp\xe4\xe4 vuoroa?', max_length=15, verbose_name='Toivottu ty\xf6vuoron pituus', choices=[('minimi', 'Yksi pitk\xc3\xa4 vuoro'), ('montalyhytta', 'Monta lyhyemp\xc3\xa4\xc3\xa4 vuoroa'), ('kaikkikay', 'Kumpi tahansa k\xc3\xa4y')]),
        ),
        migrations.AlterField(
            model_name='signupextra',
            name='total_work',
            field=models.CharField(help_text='Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana? Useimmissa teht\xe4vist\xe4 minimi on kahdeksan tuntia, mutta joissain teht\xe4viss\xe4 se voi olla my\xf6s v\xe4hemm\xe4n (esim. majoitusvalvonta 6 h).', max_length=15, verbose_name='Toivottu kokonaisty\xf6m\xe4\xe4r\xe4', choices=[('minimi', 'Haluan tehd\xc3\xa4 vain minimity\xc3\xb6panoksen (JV: 10h, muut: 8h)'), ('ekstra', 'Olen valmis tekem\xc3\xa4\xc3\xa4n lis\xc3\xa4tunteja')]),
        ),
    ]
