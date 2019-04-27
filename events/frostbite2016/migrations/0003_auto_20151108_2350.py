from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frostbite2016', '0002_desu_amount_must_be_natural'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='shirt_type',
            field=models.CharField(default='STAFF', max_length=8, verbose_name='Paidan tyyppi', choices=[('STAFF', 'Staff'), ('DESURITY', 'Desurity'), ('KUVAAJA', 'Kuvaaja'), ('VENDOR', 'Myynti')]),
        ),
    ]
