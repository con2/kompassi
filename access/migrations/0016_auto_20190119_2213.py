# Generated by Django 2.1.5 on 2019-01-19 20:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0015_auto_20170416_2044"),
    ]

    operations = [
        migrations.AddField(
            model_name="smtpserver",
            name="password_file_path_on_server",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="smtpserver",
            name="ssh_port",
            field=models.IntegerField(default=22),
        ),
        migrations.AddField(
            model_name="smtpserver",
            name="ssh_server",
            field=models.CharField(
                blank=True,
                help_text="If set, whenever the SMTP passwords for this server are changed, Kompassi will SSH to the server and write the password file on the server.",
                max_length=255,
                verbose_name="SSH server",
            ),
        ),
        migrations.AddField(
            model_name="smtpserver",
            name="ssh_username",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="smtpserver",
            name="trigger_file_path_on_server",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
