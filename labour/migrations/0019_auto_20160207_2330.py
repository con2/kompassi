# Generated by Django 1.9.1 on 2016-02-07 21:30


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0018_auto_20160202_2235"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobCategoryManagementProxy",
            fields=[],
            options={
                "proxy": True,
            },
            bases=("labour.jobcategory",),
        ),
        migrations.AlterModelOptions(
            name="jobcategory",
            options={
                "ordering": ("event", "name"),
                "verbose_name": "job category",
                "verbose_name_plural": "job categories",
            },
        ),
        migrations.AlterField(
            model_name="jobcategory",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="This descriptions will be shown to the applicants on the signup form. If there are specific requirements to this job category, please mention them here.",
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="jobcategory",
            name="event",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.Event", verbose_name="event"),
        ),
        migrations.AlterField(
            model_name="jobcategory",
            name="name",
            field=models.CharField(max_length=63, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="jobcategory",
            name="personnel_classes",
            field=models.ManyToManyField(
                blank=True,
                help_text="For most job categories, you should select the 'worker' and 'underofficer' classes here, if applicable.",
                to="labour.PersonnelClass",
                verbose_name="Personnel classes",
            ),
        ),
        migrations.AlterField(
            model_name="jobcategory",
            name="public",
            field=models.BooleanField(
                default=True,
                help_text="Job categories that are not accepting applications are not shown on the signup form. However, they may still be applied to using alternative signup forms.",
                verbose_name="Publicly accepting applications",
            ),
        ),
        migrations.AlterField(
            model_name="jobcategory",
            name="required_qualifications",
            field=models.ManyToManyField(blank=True, to="labour.Qualification", verbose_name="Required qualifications"),
        ),
        migrations.AlterField(
            model_name="laboureventmeta",
            name="registration_closes",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Registration closes"),
        ),
        migrations.AlterField(
            model_name="laboureventmeta",
            name="registration_opens",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Registration opens"),
        ),
    ]
