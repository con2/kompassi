# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nexmo', '__first__'),
        ('core', '0003_auto_20150813_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hotword', models.CharField(help_text='T\xe4ll\xe4 nimell\xe4 erotat hotwordin muista, esim. toisen tapahtuman AMV-\xe4\xe4nestyksest\xe4', max_length=255, verbose_name='Hotwordin kuvaus')),
                ('slug', models.SlugField(help_text='T\xe4m\xe4 tekstinp\xe4tk\xe4 on varsinainen avainsana, joka tulee l\xf6yty\xe4 tekstiviestist\xe4. Kirjoita pienill\xe4!', verbose_name='Avainsana')),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('assigned_event', models.ForeignKey(on_delete=models.CASCADE, to='core.Event')),
            ],
            options={
                'verbose_name': 'Hotwordi',
                'verbose_name_plural': 'Hotwordit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SMSEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sms_enabled', models.BooleanField(default=False)),
                ('current', models.BooleanField(default=False)),
                ('used_credit', models.IntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=models.CASCADE, to='core.Event')),
            ],
            options={
                'verbose_name': 'Tekstiviestej\xe4 k\xe4ytt\xe4v\xe4 tapahtuma',
                'verbose_name_plural': 'Tekstiviestej\xe4 k\xe4ytt\xe4v\xe4t tapahtumat',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SMSMessageIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.ForeignKey(on_delete=models.CASCADE, to='nexmo.InboundMessage')),
                ('smsevent', models.ForeignKey(on_delete=models.CASCADE, to='sms.SMSEvent')),
            ],
            options={
                'verbose_name': 'Vastaanotettu viesti',
                'verbose_name_plural': 'Vastaanotetut viestit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SMSMessageOut',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('to', models.CharField(max_length=20)),
                ('event', models.ForeignKey(on_delete=models.CASCADE, to='sms.SMSEvent')),
                ('ref', models.ForeignKey(blank=True, to='nexmo.OutboundMessage', null=True)),
            ],
            options={
                'verbose_name': 'L\xe4hetetty viesti',
                'verbose_name_plural': 'L\xe4hetetyt viestit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.IntegerField()),
                ('voter', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': '\xc4\xe4ni',
                'verbose_name_plural': '\xc4\xe4net',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VoteCategories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=20)),
                ('value_min', models.IntegerField()),
                ('value_max', models.IntegerField()),
                ('mapped', models.ForeignKey(on_delete=models.CASCADE, to='sms.Hotword')),
            ],
            options={
                'verbose_name': 'Kategoria',
                'verbose_name_plural': 'Kategoriat',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='vote',
            name='category',
            field=models.ForeignKey(on_delete=models.CASCADE, to='sms.VoteCategories'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vote',
            name='hotword',
            field=models.ForeignKey(on_delete=models.CASCADE, to='sms.Hotword'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vote',
            name='message',
            field=models.ForeignKey(on_delete=models.CASCADE, to='nexmo.InboundMessage'),
            preserve_default=True,
        ),
    ]
