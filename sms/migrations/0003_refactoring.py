# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0002_refactor_smsevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nominee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Osallistuja',
                'verbose_name_plural': 'Osallistujat',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VoteCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=255, verbose_name='Kategorian kuvaus')),
                ('slug', models.SlugField(max_length=20, verbose_name='Avainsana')),
                ('primary', models.BooleanField(default=False)),
                ('hotword', models.ForeignKey(on_delete=models.CASCADE, to='sms.Hotword')),
            ],
            options={
                'verbose_name': 'Kategoria',
                'verbose_name_plural': 'Kategoriat',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='votecategories',
            name='mapped',
        ),
        migrations.AddField(
            model_name='nominee',
            name='category',
            field=models.ManyToManyField(to='sms.VoteCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nominee',
            name='vote',
            field=models.ForeignKey(on_delete=models.CASCADE, to='sms.Vote'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='vote',
            name='hotword',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='voter',
        ),
        migrations.AlterField(
            model_name='vote',
            name='category',
            field=models.ForeignKey(on_delete=models.CASCADE, to='sms.VoteCategory'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='VoteCategories',
        ),
    ]
