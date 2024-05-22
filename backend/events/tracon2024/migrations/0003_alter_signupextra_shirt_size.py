# Generated by Django 5.0.4 on 2024-05-22 19:15

from django.db import migrations, models


def change_bottle_to_no_shirt(apps, schema_editor):
    SignupExtra = apps.get_model("tracon2024", "SignupExtra")
    SignupExtra.objects.filter(shirt_size="BOTTLE").update(shirt_size="NO_SHIRT")


class Migration(migrations.Migration):
    dependencies = [
        ("tracon2024", "0002_alter_signupextra_total_work"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="shirt_size",
            field=models.CharField(
                choices=[
                    ("NO_SHIRT", "Ei paitaa"),
                    ("BOTTLE", "Juomapullo"),
                    ("XS", "XS Unisex"),
                    ("S", "S Unisex"),
                    ("M", "M Unisex"),
                    ("L", "L Unisex"),
                    ("XL", "XL Unisex"),
                    ("XXL", "2XL Unisex"),
                    ("3XL", "3XL Unisex"),
                    ("4XL", "4XL Unisex"),
                    ("5XL", "5XL Unisex"),
                    ("LF_XS", "XS Ladyfit"),
                    ("LF_S", "S Ladyfit"),
                    ("LF_M", "M Ladyfit"),
                    ("LF_L", "L Ladyfit"),
                    ("LF_XL", "XL Ladyfit"),
                    ("LF_XXL", "2XL Ladyfit"),
                    ("LF_3XL", "3XL Ladyfit"),
                    ("BAG", "Kangaskassi"),
                ],
                default="NO_SHIRT",
                help_text='Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan tai juomapullon. Valitse tässä haluatko paidan vai juomapullon, sekä paidan koko. <a href="/static/tracon2022/tracon2022_shirt_sizes.png" target="_blank" rel="noopener noreferrer">Kokotaulukko</a>',
                max_length=8,
                verbose_name="Swag-valinta",
            ),
        ),
        migrations.RunPython(change_bottle_to_no_shirt),
        migrations.AlterField(
            model_name="signupextra",
            name="shirt_size",
            field=models.CharField(
                choices=[
                    ("NO_SHIRT", "Ei paitaa"),
                    ("XS", "XS Unisex"),
                    ("S", "S Unisex"),
                    ("M", "M Unisex"),
                    ("L", "L Unisex"),
                    ("XL", "XL Unisex"),
                    ("XXL", "2XL Unisex"),
                    ("3XL", "3XL Unisex"),
                    ("4XL", "4XL Unisex"),
                    ("5XL", "5XL Unisex"),
                    ("LF_XS", "XS Ladyfit"),
                    ("LF_S", "S Ladyfit"),
                    ("LF_M", "M Ladyfit"),
                    ("LF_L", "L Ladyfit"),
                    ("LF_XL", "XL Ladyfit"),
                    ("LF_XXL", "2XL Ladyfit"),
                    ("LF_3XL", "3XL Ladyfit"),
                    ("BAG", "Kangaskassi"),
                ],
                default="NO_SHIRT",
                help_text='Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan tai juomapullon. Valitse tässä haluatko paidan vai juomapullon, sekä paidan koko. <a href="/static/tracon2022/tracon2022_shirt_sizes.png" target="_blank" rel="noopener noreferrer">Kokotaulukko</a>',
                max_length=8,
                verbose_name="Swag-valinta",
            ),
        ),
    ]
