from django.db import migrations, models


def populate_accommodation_limit_group(apps, schema_editor):
    AccommodationInformation = apps.get_model("tickets", "accommodationinformation")

    for info in AccommodationInformation.objects.all():
        info.limit_groups = info.order_product.product.limit_groups.all()
        info.save()


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0008_auto_20151108_1905"),
    ]

    operations = [
        migrations.AddField(
            model_name="accommodationinformation",
            name="limit_groups",
            field=models.ManyToManyField(
                related_name="accommodation_information_set", to="tickets.LimitGroup", blank=True
            ),
        ),
        migrations.AlterField(
            model_name="accommodationinformation",
            name="order_product",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="accommodation_information_set",
                blank=True,
                to="tickets.OrderProduct",
                null=True,
            ),
        ),
        migrations.RunPython(populate_accommodation_limit_group, elidable=True),
    ]
