# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labour', '0007_jobcategory_personnel_classes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Night',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('name', models.CharField(max_length=63, help_text='')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SignupExtra',
            fields=[
                ('signup', models.OneToOneField(on_delete=models.CASCADE, primary_key=True,
                 serialize=False, help_text='', related_name='+', to='labour.Signup')),
                ('shift_type', models.CharField(verbose_name='Toivottu ty\xf6vuoron pituus', max_length=15, choices=[('yksipitka', 'Yksi pitk\xc3\xa4 vuoro'), ('montalyhytta', 'Monta lyhyemp\xc3\xa4\xc3\xa4 vuoroa'), ('kaikkikay', 'Kumpi tahansa k\xc3\xa4y')], help_text='Haluatko tehd\xe4 yhden pitk\xe4n ty\xf6vuoron vaiko monta lyhyemp\xe4\xe4 vuoroa?')),
                ('total_work', models.CharField(verbose_name='Toivottu kokonaisty\xf6m\xe4\xe4r\xe4', max_length=15, choices=[('8h', 'Minimi - 8 tuntia (1 l\xc3\xa4mmin ateria)'), ('12h', '12 tuntia (2 l\xc3\xa4mmint\xc3\xa4 ateriaa)'), ('yli12h', 'Ty\xc3\xb6n Sankari! Yli 12 tuntia! (2 l\xc3\xa4mmint\xc3\xa4 ateriaa)')], help_text='Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana? Useimmissa teht\xe4vist\xe4 minimi on kahdeksan tuntia, mutta joissain teht\xe4viss\xe4 se voi olla my\xf6s v\xe4hemm\xe4n (esim. majoitusvalvonta 6 h).')),
                ('construction', models.BooleanField(verbose_name='Voin osallistua perjantain kasaustalkoisiin', default=False, help_text='Kasaustalkoisiin osallistumista ei lasketa tapahtuman aikaiseen kokonaisty\xf6m\xe4\xe4r\xe4\xe4n.')),
                ('want_certificate', models.BooleanField(verbose_name='Haluan todistuksen ty\xf6skentelyst\xe4ni Animeconissa', default=False, help_text='')),
                ('certificate_delivery_address', models.TextField(verbose_name='Ty\xf6todistuksen toimitusosoite', blank=True, help_text='Jos haluat ty\xf6todistuksen, t\xe4yt\xe4 t\xe4h\xe4n kentt\xe4\xe4n postiosoite (katuosoite, postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.')),
                ('shirt_size', models.CharField(verbose_name='Paidan koko', max_length=8, choices=[('NO_SHIRT', 'Ei paitaa'), ('XS', 'XS Unisex'), ('S', 'S Unisex'), ('M', 'M Unisex'), ('L', 'L Unisex'), ('XL', 'XL Unisex'), ('XXL', 'XXL Unisex'), ('3XL', '3XL Unisex'), ('4XL', '4XL Unisex'), ('5XL', '5XL Unisex'), ('LF_XS', 'XS Ladyfit'), ('LF_S', 'S Ladyfit'), ('LF_M', 'M Ladyfit'), ('LF_L', 'L Ladyfit'), ('LF_XL', 'XL Ladyfit')], help_text='')),
                ('special_diet_other', models.TextField(verbose_name='Muu erikoisruokavalio', blank=True, help_text='Jos noudatat erikoisruokavaliota, jota ei ole yll\xe4 olevassa listassa, ilmoita se t\xe4ss\xe4. Tapahtuman j\xe4rjest\xe4j\xe4 pyrkii ottamaan erikoisruokavaliot huomioon, mutta kaikkia erikoisruokavalioita ei v\xe4ltt\xe4m\xe4tt\xe4 pystyt\xe4 j\xe4rjest\xe4m\xe4\xe4n.')),
                ('prior_experience', models.TextField(verbose_name='Ty\xf6kokemus', blank=True, help_text='Kerro t\xe4ss\xe4 kent\xe4ss\xe4, jos sinulla on aiempaa kokemusta vastaavista teht\xe4vist\xe4 tai muuta sellaista ty\xf6kokemusta, josta arvioit olevan hy\xf6ty\xe4 hakemassasi teht\xe4v\xe4ss\xe4.')),
                ('free_text', models.TextField(verbose_name='Vapaa alue', blank=True, help_text='Jos haluat sanoa hakemuksesi k\xe4sittelij\xf6ille jotain sellaista, jolle ei ole omaa kentt\xe4\xe4 yll\xe4, k\xe4yt\xe4 t\xe4t\xe4 kentt\xe4\xe4.')),
                ('lodging_needs', models.ManyToManyField(verbose_name='Tarvitsen lattiamajoitusta', blank=True, help_text='Ruksaa ne y\xf6t, joille tarvitset lattiamajoitusta. Lattiamajoitus sijaitsee k\xe4velymatkan p\xe4\xe4ss\xe4 tapahtumapaikalta.', to='animecon2015.Night')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecialDiet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('name', models.CharField(max_length=63, help_text='')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='signupextra',
            name='special_diet',
            field=models.ManyToManyField(verbose_name='Erikoisruokavalio', blank=True, help_text='', to='animecon2015.SpecialDiet'),
            preserve_default=True,
        ),
    ]
