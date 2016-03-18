# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 18:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labour', '0021_auto_20160306_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Night',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SignupExtra',
            fields=[
                ('signup', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='animecon2016_signup_extra', serialize=False, to='labour.Signup')),
                ('total_work', models.CharField(choices=[('minimi', 'Haluan tehd\xe4 vain minimity\xf6panoksen (JV: 10h, muut: 8h)'), ('ekstra', 'Olen valmis tekem\xe4\xe4n lis\xe4tunteja')], help_text='Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana?', max_length=15, verbose_name='Toivottu kokonaisty\xf6m\xe4\xe4r\xe4')),
                ('personal_identification_number', models.CharField(blank=True, default='', help_text='HUOM! T\xe4yt\xe4 t\xe4m\xe4 kentt\xe4 vain, jos haet <strong>kortittomaksi j\xe4rjestyksenvalvojaksi</strong>.', max_length=12, verbose_name='Henkil\xf6tunnus')),
                ('want_certificate', models.BooleanField(default=False, verbose_name='Haluan todistuksen ty\xf6skentelyst\xe4ni Animeconissa')),
                ('certificate_delivery_address', models.TextField(blank=True, help_text='Jos haluat ty\xf6todistuksen, t\xe4yt\xe4 t\xe4h\xe4n kentt\xe4\xe4n postiosoite (katuosoite, postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.', verbose_name='Ty\xf6todistuksen toimitusosoite')),
                ('special_diet_other', models.TextField(blank=True, help_text='Jos noudatat erikoisruokavaliota, jota ei ole yll\xe4 olevassa listassa, ilmoita se t\xe4ss\xe4. Tapahtuman j\xe4rjest\xe4j\xe4 pyrkii ottamaan erikoisruokavaliot huomioon, mutta kaikkia erikoisruokavalioita ei v\xe4ltt\xe4m\xe4tt\xe4 pystyt\xe4 j\xe4rjest\xe4m\xe4\xe4n.', verbose_name='Muu erikoisruokavalio')),
                ('prior_experience', models.TextField(blank=True, help_text='Kerro t\xe4ss\xe4 kent\xe4ss\xe4, jos sinulla on aiempaa kokemusta vastaavista teht\xe4vist\xe4 tai muuta sellaista ty\xf6kokemusta, josta arvioit olevan hy\xf6ty\xe4 hakemassasi teht\xe4v\xe4ss\xe4.', verbose_name='Ty\xf6kokemus')),
                ('free_text', models.TextField(blank=True, help_text='Jos haluat sanoa hakemuksesi k\xe4sittelij\xf6ille jotain sellaista, jolle ei ole omaa kentt\xe4\xe4 yll\xe4, k\xe4yt\xe4 t\xe4t\xe4 kentt\xe4\xe4.', verbose_name='Vapaa alue')),
                ('lodging_needs', models.ManyToManyField(blank=True, help_text='Ruksaa ne y\xf6t, joille tarvitset lattiamajoitusta. Lattiamajoitus sijaitsee k\xe4velymatkan p\xe4\xe4ss\xe4 tapahtumapaikalta.', to='animecon2016.Night', verbose_name='Tarvitsen lattiamajoitusta')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpecialDiet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='signupextra',
            name='special_diet',
            field=models.ManyToManyField(blank=True, to='animecon2016.SpecialDiet', verbose_name='Erikoisruokavalio'),
        ),
    ]
