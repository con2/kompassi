# Generated by Django 4.2.6 on 2023-11-08 18:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("surveys", "0004_auto_20190909_2157"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventsurveyresult",
            name="author",
        ),
        migrations.RemoveField(
            model_name="eventsurveyresult",
            name="survey",
        ),
        migrations.RemoveField(
            model_name="globalsurvey",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="globalsurveyresult",
            name="author",
        ),
        migrations.RemoveField(
            model_name="globalsurveyresult",
            name="survey",
        ),
        migrations.DeleteModel(
            name="EventSurvey",
        ),
        migrations.DeleteModel(
            name="EventSurveyResult",
        ),
        migrations.DeleteModel(
            name="GlobalSurvey",
        ),
        migrations.DeleteModel(
            name="GlobalSurveyResult",
        ),
    ]
