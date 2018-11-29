# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labour', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Night',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=63)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SignupExtra',
            fields=[
                ('signup', models.OneToOneField(on_delete=models.CASCADE, related_name='+', primary_key=True, serialize=False, to='labour.Signup')),
                ('shift_type', models.CharField(help_text='Haluatko tehd\xe4 yhden pitk\xe4n ty\xf6vuoron vaiko monta lyhyemp\xe4\xe4 vuoroa?', max_length=15, verbose_name='Toivottu ty\xf6vuoron pituus', choices=[('yksipitka', 'Yksi pitk\xc3\xa4 vuoro'), ('montalyhytta', 'Monta lyhyemp\xc3\xa4\xc3\xa4 vuoroa'), ('kaikkikay', 'Kumpi tahansa k\xc3\xa4y')])),
                ('total_work', models.CharField(help_text='Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana? Useimmissa teht\xe4vist\xe4 minimi on kahdeksan tuntia, mutta joissain teht\xe4viss\xe4 se voi olla my\xf6s v\xe4hemm\xe4n (esim. majoitusvalvonta 6 h).', max_length=15, verbose_name='Toivottu kokonaisty\xf6m\xe4\xe4r\xe4', choices=[('8h', 'Minimi - 8 tuntia (1 l\xc3\xa4mmin ateria)'), ('12h', '12 tuntia (2 l\xc3\xa4mmint\xc3\xa4 ateriaa)'), ('yli12h', 'Ty\xc3\xb6n Sankari! Yli 12 tuntia! (2 l\xc3\xa4mmint\xc3\xa4 ateriaa)')])),
                ('construction', models.BooleanField(default=False, help_text='Kasaustalkoisiin osallistumista ei lasketa tapahtuman aikaiseen kokonaisty\xf6m\xe4\xe4r\xe4\xe4n.', verbose_name='Voin osallistua perjantain kasaustalkoisiin')),
                ('overseer', models.BooleanField(default=False, help_text='Yliv\xe4nk\xe4rit eli kersantit ovat kokeneempia conity\xf6l\xe4isi\xe4, jotka toimivat oman teht\xe4v\xe4alueensa tiiminvet\xe4j\xe4n\xe4.', verbose_name='Olen kiinnostunut v\xe4nk\xe4rikersantin teht\xe4vist\xe4')),
                ('want_certificate', models.BooleanField(default=False, verbose_name='Haluan todistuksen ty\xf6skentelyst\xe4ni Traconissa')),
                ('certificate_delivery_address', models.TextField(help_text='Jos haluat ty\xf6todistuksen, t\xe4yt\xe4 t\xe4h\xe4n kentt\xe4\xe4n postiosoite (katuosoite, postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.', verbose_name='Ty\xf6todistuksen toimitusosoite', blank=True)),
                ('shirt_size', models.CharField(max_length=8, verbose_name='Paidan koko', choices=[('NO_SHIRT', 'Ei paitaa'), ('XS', 'XS Unisex'), ('S', 'S Unisex'), ('M', 'M Unisex'), ('L', 'L Unisex'), ('XL', 'XL Unisex'), ('XXL', 'XXL Unisex'), ('3XL', '3XL Unisex'), ('4XL', '4XL Unisex'), ('5XL', '5XL Unisex'), ('LF_XS', 'XS Ladyfit'), ('LF_S', 'S Ladyfit'), ('LF_M', 'M Ladyfit'), ('LF_L', 'L Ladyfit'), ('LF_XL', 'XL Ladyfit')])),
                ('special_diet_other', models.TextField(help_text='Jos noudatat erikoisruokavaliota, jota ei ole yll\xe4 olevassa listassa, ilmoita se t\xe4ss\xe4. Tapahtuman j\xe4rjest\xe4j\xe4 pyrkii ottamaan erikoisruokavaliot huomioon, mutta kaikkia erikoisruokavalioita ei v\xe4ltt\xe4m\xe4tt\xe4 pystyt\xe4 j\xe4rjest\xe4m\xe4\xe4n.', verbose_name='Muu erikoisruokavalio', blank=True)),
                ('prior_experience', models.TextField(help_text='Kerro t\xe4ss\xe4 kent\xe4ss\xe4, jos sinulla on aiempaa kokemusta vastaavista teht\xe4vist\xe4 tai muuta sellaista ty\xf6kokemusta, josta arvioit olevan hy\xf6ty\xe4 hakemassasi teht\xe4v\xe4ss\xe4.', verbose_name='Ty\xf6kokemus', blank=True)),
                ('free_text', models.TextField(help_text='Jos haluat sanoa hakemuksesi k\xe4sittelij\xf6ille jotain sellaista, jolle ei ole omaa kentt\xe4\xe4 yll\xe4, k\xe4yt\xe4 t\xe4t\xe4 kentt\xe4\xe4.', verbose_name='Vapaa alue', blank=True)),
                ('lodging_needs', models.ManyToManyField(help_text='Ruksaa ne y\xf6t, joille tarvitset lattiamajoitusta. Lattiamajoitus sijaitsee k\xe4velymatkan p\xe4\xe4ss\xe4 tapahtumapaikalta.', to='tracon9.Night', verbose_name='Tarvitsen lattiamajoitusta', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecialDiet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=63)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='signupextra',
            name='special_diet',
            field=models.ManyToManyField(to='tracon9.SpecialDiet', verbose_name='Erikoisruokavalio', blank=True),
            preserve_default=True,
        ),
    ]
