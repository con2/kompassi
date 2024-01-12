# Generated by Django 1.9.1 on 2016-01-24 21:28


from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0014_auto_20151108_1906"),
    ]

    operations = [
        migrations.CreateModel(
            name="SignupOnboardingProxy",
            fields=[],
            options={
                "proxy": True,
            },
            bases=("labour.signup",),
        ),
        migrations.AlterModelOptions(
            name="alternativesignupform",
            options={"verbose_name": "alternative signup form", "verbose_name_plural": "alternative signup forms"},
        ),
        migrations.AlterModelOptions(
            name="infolink",
            options={"verbose_name": "info link", "verbose_name_plural": "info links"},
        ),
        migrations.AlterModelOptions(
            name="job",
            options={"verbose_name": "job", "verbose_name_plural": "jobs"},
        ),
        migrations.AlterModelOptions(
            name="jobcategory",
            options={"verbose_name": "job category", "verbose_name_plural": "job categories"},
        ),
        migrations.AlterModelOptions(
            name="jobrequirement",
            options={"verbose_name": "job requirement", "verbose_name_plural": "job requirements"},
        ),
        migrations.AlterModelOptions(
            name="laboureventmeta",
            options={"verbose_name": "labour event meta", "verbose_name_plural": "labour event metas"},
        ),
        migrations.AlterModelOptions(
            name="perk",
            options={"verbose_name": "perk", "verbose_name_plural": "perks"},
        ),
        migrations.AlterModelOptions(
            name="personnelclass",
            options={
                "ordering": ("event", "priority"),
                "verbose_name": "personnel class",
                "verbose_name_plural": "personnel classes",
            },
        ),
        migrations.AlterModelOptions(
            name="personqualification",
            options={"verbose_name": "qualification holder", "verbose_name_plural": "qualification holders"},
        ),
        migrations.AlterModelOptions(
            name="qualification",
            options={"verbose_name": "qualification", "verbose_name_plural": "qualifications"},
        ),
        migrations.AlterModelOptions(
            name="signup",
            options={"verbose_name": "signup", "verbose_name_plural": "signups"},
        ),
        migrations.AlterModelOptions(
            name="workperiod",
            options={"verbose_name": "work period", "verbose_name_plural": "work periods"},
        ),
    ]
