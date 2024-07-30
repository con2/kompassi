from django import forms
from django.contrib import admin

from .models import Entry, Subscription
from .registry import entry_types

ENTRY_READ_ONLY_FIELDS = (
    "created_at",
    "actor",
    "entry_type",
    "other_fields",
)


class MonthFilter(admin.SimpleListFilter):
    title = "month"
    parameter_name = "month"

    def lookups(self, request, model_admin):
        return (
            (f"{year}-{month:02}", f"{year}-{month:02}")
            for (year, month) in Entry.get_expected_partitions(months_future=0)
        )

    def queryset(self, request, queryset):
        if value := self.value():
            year, month = map(int, value.split("-"))
            return Entry.year_month_filter(queryset, year, month)
        return queryset


class EntryTypeFilter(admin.SimpleListFilter):
    title = "type"
    parameter_name = "type"

    def lookups(self, request, model_admin):
        return [(k, k) for k in entry_types.keys()]  # noqa: SIM118 (false positive)

    def queryset(self, request, queryset):
        if value := self.value():
            return queryset.filter(entry_type=value)
        return queryset


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("created_at", "entry_type", "message")
    raw_id_fields = ("actor",)
    fields = ENTRY_READ_ONLY_FIELDS
    readonly_fields = ENTRY_READ_ONLY_FIELDS
    list_filter = [MonthFilter, EntryTypeFilter]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class SubscriptionAdminForm(forms.ModelForm):
    entry_type = forms.ChoiceField(
        choices=lambda: [(k, k) for k in entry_types.keys()],  # noqa: SIM118 (false positive)
    )

    class Meta:
        model = Subscription
        fields = ("user", "entry_type")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "entry_type")
    list_filter = ["entry_type"]
    form = SubscriptionAdminForm
    raw_id_fields = ("user",)
