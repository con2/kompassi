from django.db import migrations


def populate_payments_organization_meta(apps, schema_editor):
    PaymentsOrganizationMeta = apps.get_model("payments", "PaymentsOrganizationMeta")
    PaymentsEventMeta = apps.get_model("payments", "PaymentsEventMeta")

    for payments_event_meta in PaymentsEventMeta.objects.all().order_by("-event__start_time"):
        PaymentsOrganizationMeta.objects.get_or_create(
            organization=payments_event_meta.event.organization,
            defaults=dict(
                checkout_merchant=payments_event_meta.checkout_merchant,
                checkout_password=payments_event_meta.checkout_password,
            ),
        )

    CheckoutPayment = apps.get_model("payments", "CheckoutPayment")
    for payment in CheckoutPayment.objects.all():
        payment.organization = payment.event.organization
        payment.save()


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0005_payments_organization_meta"),
    ]

    operations = [
        migrations.RunPython(populate_payments_organization_meta),
    ]
