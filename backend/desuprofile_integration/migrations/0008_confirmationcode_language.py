# Generated by Django 5.0.10 on 2024-12-12 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desuprofile_integration', '0007_rename_confirmationcode_person_state_desuprofile_person__372366_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmationcode',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('fi', 'Finnish'), ('sv', 'Swedish')], default='en', max_length=2),
        ),
    ]