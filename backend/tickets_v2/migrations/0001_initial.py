from decimal import Decimal
from pathlib import Path

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import core.models.group_management_mixin
import event_log_v2.utils.monthly_partitions
import event_log_v2.utils.uuid7
import tickets_v2.utils.event_partitions


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
                ("title", models.TextField()),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("available_from", models.DateTimeField(blank=True, null=True)),
                ("available_until", models.DateTimeField(blank=True, null=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, related_name="products", to="core.event"
                    ),
                ),
                (
                    "superseded_by",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to="tickets_v2.product"
                    ),
                ),
                ("quotas", models.ManyToManyField(related_name="products", to="tickets_v2.quota")),
            ],
        ),
        migrations.RunSQL(
            sql=Path(__file__).with_name("0001_initial_partitioned_tables.sql").read_text(),
            reverse_sql="""
            drop table if exists tickets_v2_ticket cascade;
            drop table if exists tickets_v2_order cascade;
            """,
            state_operations=[
                migrations.CreateModel(
                    name="Order",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=event_log_v2.utils.uuid7.uuid7,
                                editable=False,
                                primary_key=True,  # cheating!
                                serialize=False,
                            ),
                        ),
                        ("first_name", models.TextField()),
                        ("last_name", models.TextField()),
                        ("phone", models.TextField()),
                        ("email", models.EmailField()),
                        ("product_data", models.JSONField(default=dict, help_text="product id -> quantity")),
                        ("paid_at", models.DateTimeField(blank=True, null=True)),
                        ("cancelled_at", models.DateTimeField(blank=True, null=True)),
                        ("cached_price", models.DecimalField(decimal_places=2, default=Decimal("0"), max_digits=10)),
                        (
                            "event",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.RESTRICT, related_name="+", to="core.event"
                            ),
                        ),
                        (
                            "user",
                            models.ForeignKey(
                                blank=True,
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="+",
                                to=settings.AUTH_USER_MODEL,
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
                    name="Ticket",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=event_log_v2.utils.uuid7.uuid7,
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
            ],
        ),
    ]
