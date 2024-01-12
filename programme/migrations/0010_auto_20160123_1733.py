# Generated by Django 1.9.1 on 2016-01-23 15:33


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0009_auto_20160123_1336"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name="Created at"),
        ),
        migrations.AddField(
            model_name="programme",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="invitation",
            name="email",
            field=models.CharField(max_length=1023, verbose_name="E-mail address"),
        ),
        migrations.AlterField(
            model_name="invitation",
            name="programme",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="programme.Programme", verbose_name="Programme"
            ),
        ),
        migrations.AlterField(
            model_name="invitation",
            name="role",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="programme.Role", verbose_name="Role"
            ),
        ),
    ]
