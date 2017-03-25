# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frostbite2016', '0003_auto_20151108_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='shirt_size',
            field=models.CharField(default='NO_SHIRT', help_text='Ajoissa ilmoittautuneet v\xe4nk\xe4rit saavat maksuttoman ty\xf6voimapaidan. Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" target="_blank">ladyfit-paita</a>', max_length=8, verbose_name='Paidan koko', choices=[('NO_SHIRT', 'Ei paitaa'), ('XS', 'XS Unisex'), ('S', 'S Unisex'), ('M', 'M Unisex'), ('L', 'L Unisex'), ('XL', 'XL Unisex'), ('XXL', 'XXL Unisex'), ('3XL', '3XL Unisex'), ('4XL', '4XL Unisex'), ('5XL', '5XL Unisex'), ('LF_XS', 'XS Ladyfit'), ('LF_S', 'S Ladyfit'), ('LF_M', 'M Ladyfit'), ('LF_L', 'L Ladyfit'), ('LF_XL', 'XL Ladyfit')]),
        ),
        migrations.AlterField(
            model_name='signupextra',
            name='shirt_type',
            field=models.CharField(default='TOOLATE', max_length=8, verbose_name='Paidan tyyppi', choices=[('STAFF', 'Staff'), ('DESURITY', 'Desurity'), ('KUVAAJA', 'Kuvaaja'), ('VENDOR', 'Myynti'), ('TOOLATE', 'My\xf6h\xe4styi paitatilauksesta')]),
        ),
    ]
