from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0003_populate_pclasses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signup",
            name="personnel_classes",
            field=models.ManyToManyField(
                help_text="Mihin henkil\xf6st\xf6ryhmiin t\xe4m\xe4 henkil\xf6 kuuluu? Henkil\xf6 saa valituista ryhmist\xe4 ylimm\xe4n mukaisen badgen. L\xe4ht\xf6kohtaisesti t\xe4t\xe4 tietoa ei tulisi muokata k\xe4sin.",
                to="labour.PersonnelClass",
                verbose_name="Yhteiskuntaluokat",
                blank=True,
            ),
        ),
    ]
