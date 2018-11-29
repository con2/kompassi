# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labour', '0008_auto_20150419_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignupExtra',
            fields=[
                ('signup', models.OneToOneField(on_delete=models.CASCADE,
                 related_name='+', primary_key=True, serialize=False, to='labour.Signup')),
                ('shift_type', models.CharField(help_text='Haluatko tehd\xe4 yhden pitk\xe4n ty\xf6vuoron vaiko monta lyhyemp\xe4\xe4 vuoroa?', max_length=15, verbose_name='Toivottu ty\xf6vuoron pituus', choices=[('none', 'Ei v\xe4li\xe4'), ('4h', 'Pari pitk\xe4\xe4 vuoroa'), ('yli4h', 'Useita lyhyit\xe4 vuoroja')])),
                ('desu_amount', models.IntegerField(help_text='Kuinka monessa Desuconissa olet ollut v\xe4nk\xe4rin\xe4?', verbose_name='Desum\xe4\xe4r\xe4')),
                ('prior_experience', models.TextField(help_text='Kerro t\xe4ss\xe4 kent\xe4ss\xe4, jos sinulla on aiempaa kokemusta vastaavista teht\xe4vist\xe4 tai muuta sellaista ty\xf6kokemusta, josta arvioit olevan hy\xf6ty\xe4 hakemassasi teht\xe4v\xe4ss\xe4.', verbose_name='Ty\xf6kokemus', blank=True)),
                ('free_text', models.TextField(help_text='Jos haluat sanoa hakemuksesi k\xe4sittelij\xf6ille jotain sellaista, jolle ei ole omaa kentt\xe4\xe4 yll\xe4, k\xe4yt\xe4 t\xe4t\xe4 kentt\xe4\xe4.Jos haet valokuvaajaksi, kerro lis\xe4ksi millaista kuvauskalustoa sinulla on k\xe4ytett\xe4viss\xe4si ja listaamuutamia gallerialinkkej\xe4, joista p\xe4\xe4semme ihailemaan ottamiasi kuvia.', verbose_name='Vapaa alue', blank=True)),
                ('shirt_size', models.CharField(help_text='Ajoissa ilmoittautuneet v\xe4nk\xe4rit saavat maksuttoman ty\xf6voimapaidan. Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" target="_blank">ladyfit-paita</a>', max_length=8, verbose_name='Paidan koko', choices=[('NO_SHIRT', 'Ei paitaa'), ('XS', 'XS Unisex'), ('S', 'S Unisex'), ('M', 'M Unisex'), ('L', 'L Unisex'), ('XL', 'XL Unisex'), ('XXL', 'XXL Unisex'), ('3XL', '3XL Unisex'), ('4XL', '4XL Unisex'), ('5XL', '5XL Unisex'), ('LF_XS', 'XS Ladyfit'), ('LF_S', 'S Ladyfit'), ('LF_M', 'M Ladyfit'), ('LF_L', 'L Ladyfit'), ('LF_XL', 'XL Ladyfit')])),
                ('shirt_type', models.CharField(default='STAFF', max_length=8, verbose_name='Paidan tyyppi', choices=[('STAFF', 'Staff'), ('DESURITY', 'Desurity'), ('VENDOR', 'Myynti')])),
                ('night_work', models.BooleanField(default=False, verbose_name='Olen valmis tekem\xe4\xe4n y\xf6t\xf6it\xe4')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
