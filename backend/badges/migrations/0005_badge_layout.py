from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("badges", "0004_remove_template"),
    ]

    operations = [
        migrations.AddField(
            model_name="badgeseventmeta",
            name="badge_layout",
            field=models.CharField(
                default="trad",
                help_text="Perinteinen: teht\xe4v\xe4nimike, etunimi sukunimi, nick. Nicki\xe4 korostava: nick tai etunimi, sukunimi tai koko nimi, teht\xe4v\xe4nimike.",
                max_length=4,
                verbose_name="Badgen asettelu",
                choices=[("trad", "Perinteinen"), ("nick", "Nicki\xe4 korostava")],
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="badge",
            name="personnel_class",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                verbose_name="Henkil\xf6st\xf6luokka",
                blank=True,
                to="labour.PersonnelClass",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="badgeseventmeta",
            name="badge_factory_code",
            field=models.CharField(
                default="badges.utils:default_badge_factory",
                help_text="Funktio, joka selvitt\xe4\xe4, mink\xe4 tyyppinen badge henkil\xf6lle pit\xe4isi luoda. Oletusarvo toimii l\xe4hes kaikille tapahtumille.",
                max_length=255,
                verbose_name="Badgetehdas",
            ),
            preserve_default=True,
        ),
    ]
