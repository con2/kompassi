from decimal import Decimal
from pathlib import Path

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import core.models.group_management_mixin
import event_log_v2.utils.monthly_partitions
import tickets_v2.optimized_server.utils.uuid7
import tickets_v2.utils.event_partitions

PAYMENT_STATUS_CHOICES = [
    (0, "NOT_STARTED"),
    (1, "PENDING"),
    (2, "FAILED"),
    (3, "PAID"),
    (4, "CANCELLED"),
    (5, "REFUND_REQUESTED"),
    (6, "REFUND_FAILED"),
    (7, "REFUNDED"),
]


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("core", "0040_rename_emailverificationtoken_person_state_core_emailv_person__722147_idx_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TicketsV2EventMeta",
            fields=[
                (
                    "event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="%(class)s",
                        serialize=False,
                        to="core.event",
                    ),
                ),
                ("admin_group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="auth.group")),
                (
                    "provider_id",
                    models.SmallIntegerField(
                        choices=[(0, "NONE"), (1, "PAYTRAIL"), (2, "STRIPE")],
                        default=0,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, core.models.group_management_mixin.GroupManagementMixin),
        ),
        migrations.CreateModel(
            name="Quota",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.TextField()),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="quotas", to="core.event"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, related_name="products", to="core.event"
                    ),
                ),
                ("max_per_order", models.PositiveSmallIntegerField(default=5)),
                ("etickets_per_product", models.PositiveSmallIntegerField(default=1)),
                (
                    "superseded_by",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to="tickets_v2.product"
                    ),
                ),
                ("available_from", models.DateTimeField(blank=True, null=True)),
                ("available_until", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("title", models.TextField()),
                ("description", models.TextField()),
                ("quotas", models.ManyToManyField(related_name="products", to="tickets_v2.quota")),
            ],
        ),
        migrations.RunSQL(
            sql=Path(__file__).with_name("0001_initial.sql").read_text(),
            reverse_sql="""
                drop table if exists tickets_v2_receipt cascade;
                drop table if exists tickets_v2_paymentstamp cascade;
                drop table if exists tickets_v2_ticket cascade;
                drop table if exists tickets_v2_order cascade;

                drop domain if exists tickets_v2_paymentprovider;
                drop domain if exists tickets_v2_paymentstamptype;
                drop domain if exists tickets_v2_paymentstatus;
                drop domain if exists tickets_v2_receipttype;
                drop domain if exists tickets_v2_receiptstatus;
            """,
            state_operations=[
                migrations.CreateModel(
                    name="Order",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=tickets_v2.optimized_server.utils.uuid7.uuid7,
                                editable=False,
                                primary_key=True,  # cheating!
                                serialize=False,
                            ),
                        ),
                        (
                            "event",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.RESTRICT,
                                related_name="+",
                                to="core.event",
                            ),
                        ),
                        (
                            "order_number",
                            models.IntegerField(
                                help_text=(
                                    "Order number used in contexts where UUID cannot be used. "
                                    "Such places include generating reference numbers and "
                                    "the customer reading the order number aloud to an event rep. "
                                    "Prefer id (UUID) for everything else (eg. URLs)."
                                )
                            ),
                        ),
                        (
                            "owner",
                            models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name="+",
                            ),
                        ),
                        (
                            "cached_status",
                            models.SmallIntegerField(
                                choices=PAYMENT_STATUS_CHOICES,
                                default=0,
                                help_text="Payment status of the order. Updated by a trigger on PaymentStamp.",
                            ),
                        ),
                        (
                            "cached_price",
                            models.DecimalField(
                                decimal_places=2,
                                default=Decimal("0"),
                                help_text="Total price of the order in euros. Calculated by create_order.sql from product_data.",
                                max_digits=10,
                            ),
                        ),
                        (
                            "language",
                            models.CharField(
                                choices=[("en", "English"), ("fi", "Finnish"), ("sv", "Swedish")],
                                max_length=2,
                            ),
                        ),
                        (
                            "product_data",
                            models.JSONField(
                                default=dict,
                                help_text="product id -> quantity",
                            ),
                        ),
                        ("first_name", models.TextField()),
                        ("last_name", models.TextField()),
                        ("email", models.EmailField()),
                        ("phone", models.TextField(blank=True, default="")),
                    ],
                    bases=(
                        tickets_v2.utils.event_partitions.EventPartitionsMixin,
                        event_log_v2.utils.monthly_partitions.UUID7Mixin,
                        models.Model,
                    ),
                ),
                migrations.CreateModel(
                    name="Ticket",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=tickets_v2.optimized_server.utils.uuid7.uuid7,
                                editable=False,
                                primary_key=True,  # cheating!
                                serialize=False,
                            ),
                        ),
                        ("order_id", models.UUIDField(null=True, blank=True)),
                        (
                            "event",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.RESTRICT, related_name="+", to="core.event"
                            ),
                        ),
                        (
                            "quota",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE, related_name="+", to="tickets_v2.quota"
                            ),
                        ),
                    ],
                    bases=(
                        tickets_v2.utils.event_partitions.EventPartitionsMixin,
                        event_log_v2.utils.monthly_partitions.UUID7Mixin,
                        models.Model,
                    ),
                ),
                migrations.CreateModel(
                    name="PaymentStamp",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=tickets_v2.optimized_server.utils.uuid7.uuid7,
                                editable=False,
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        (
                            "order_id",
                            models.UUIDField(
                                blank=True,
                                null=True,
                            ),
                        ),
                        (
                            "correlation_id",
                            models.UUIDField(
                                help_text="The correlation ID ties together the payment stamps related to the same payment attempt. For Paytrail, this is what they call 'stamp'."
                            ),
                        ),
                        (
                            "provider_id",
                            models.SmallIntegerField(
                                choices=[
                                    (0, "NONE"),
                                    (1, "PAYTRAIL"),
                                    (2, "STRIPE"),
                                ],
                            ),
                        ),
                        (
                            "type",
                            models.SmallIntegerField(
                                choices=[
                                    (0, "ZERO_PRICE"),
                                    (1, "CREATE_PAYMENT_REQUEST"),
                                    (2, "CREATE_PAYMENT_SUCCESS"),
                                    (3, "CREATE_PAYMENT_FAILURE"),
                                    (4, "PAYMENT_REDIRECT"),
                                    (5, "PAYMENT_CALLBACK"),
                                ],
                            ),
                        ),
                        (
                            "status",
                            models.SmallIntegerField(
                                choices=PAYMENT_STATUS_CHOICES,
                            ),
                        ),
                        (
                            "data",
                            models.JSONField(
                                help_text="What we sent to or received from the payment provider_id. Sensitive details such as API credentials, PII etc. may be redacted. Also fields lifted to relational fields need not be repeated here."
                            ),
                        ),
                        (
                            "event",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.RESTRICT, related_name="+", to="core.event"
                            ),
                        ),
                    ],
                    bases=(
                        tickets_v2.utils.event_partitions.EventPartitionsMixin,
                        event_log_v2.utils.monthly_partitions.UUID7Mixin,
                        models.Model,
                    ),
                ),
                migrations.CreateModel(
                    name="Receipt",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=tickets_v2.optimized_server.utils.uuid7.uuid7,
                                editable=False,
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        (
                            "event",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.RESTRICT,
                                related_name="+",
                                to="core.event",
                            ),
                        ),
                        (
                            "order_id",
                            models.UUIDField(
                                blank=True,
                                null=True,
                            ),
                        ),
                        (
                            "correlation_id",
                            models.UUIDField(
                                help_text="The correlation ID ties together the receipt stamps related to the same receipt attempt. Usually you would use the correlation ID of the payment stamp that you used to determine this order is paid."
                            ),
                        ),
                        (
                            "batch_id",
                            models.UUIDField(
                                null=True,
                                blank=True,
                                help_text=(
                                    "The ID of the batch this receipt was sent processed in. "
                                    "This is an UUIDv7 that is generated when the batch is created. "
                                    "If the receipt is stuck in PROCESSING and the batch ID is old, then the batch has probably failed and needs to be retried."
                                ),
                            ),
                        ),
                        (
                            "type",
                            models.SmallIntegerField(
                                choices=[
                                    (1, "ORDER_CONFIRMATION"),
                                    (2, "CANCELLATION"),
                                ],
                            ),
                        ),
                        (
                            "status",
                            models.SmallIntegerField(
                                choices=[
                                    (0, "REQUESTED"),
                                    (1, "PROCESSING"),
                                    (2, "FAILURE"),
                                    (3, "SUCCESS"),
                                ],
                            ),
                        ),
                        (
                            "email",
                            models.EmailField(
                                blank=True,
                                default="",
                                help_text="The email address to which the receipt was sent.",
                                max_length=254,
                            ),
                        ),
                    ],
                    bases=(
                        tickets_v2.utils.event_partitions.EventPartitionsMixin,
                        event_log_v2.utils.monthly_partitions.UUID7Mixin,
                        models.Model,
                    ),
                ),
            ],
        ),
    ]
