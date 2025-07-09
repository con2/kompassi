import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from tickets_v2.optimized_server.utils import uuid7


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                create table event_log_v2_entry (
                    id uuid primary key,
                    actor_id integer,
                    entry_type varchar(255) not null,
                    other_fields jsonb not null default '{}',
                    foreign key (actor_id) references auth_user (id) on delete set null
                ) partition by range (id)
            """,  # XXX not actually swappable
            reverse_sql="drop table event_log_v2_entry",
            state_operations=[
                migrations.CreateModel(
                    name="Entry",
                    fields=[
                        (
                            "id",
                            models.UUIDField(
                                default=uuid7.uuid7,  # type: ignore
                                editable=False,
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        ("entry_type", models.CharField(max_length=255)),
                        ("other_fields", models.JSONField(blank=True, default=dict)),
                        (
                            "actor",
                            models.ForeignKey(
                                blank=True,
                                db_index=False,
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="access_log_entries",
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                    ],
                    options={
                        "ordering": ("id",),
                    },
                ),
            ],
        )
    ]
