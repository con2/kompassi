from django import forms
from django.contrib import admin
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .models import (
    AlternativeProgrammeForm,
    Category,
    Programme,
    ProgrammeFeedback,
    Role,
    Room,
    SpecialReservation,
    SpecialStartTime,
    Tag,
    TimeBlock,
    View,
    ViewRoom,
)
from .proxies.freeform_organizer.admin import FreeformOrganizerAdminProxy


@admin.action(description=_("Deactivate selected items"))
def deactivate_selected_items(modeladmin, request, queryset):
    queryset.update(active=False)


@admin.action(description=_("Activate selected items"))
def activate_selected_items(modeladmin, request, queryset):
    queryset.update(active=False)


class ProgrammeRoleInline(admin.TabularInline):
    model = Programme.organizers.through
    verbose_name = "organizer"
    verbose_name_plural = "organizers"


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "category",
        "state",
        "room",
        "start_time",
        "length",
        "end_time",
        "paikkala_icon",
        "is_paikkala_public",
        "is_paikkala_time_visible",
        "hosts_from_host",
    )
    readonly_fields = (
        "title",
        "category",
        "state",
        "room",
        "start_time",
        "length",
        "end_time",
    )
    list_display = ("title", "category", "room", "start_time", "length", "end_time")
    list_filter = ("category__event",)
    search_fields = ("title",)


class ProgrammeInline(admin.TabularInline):
    model = Programme
    fields = ("title", "category", "room", "start_time", "length", "end_time")
    readonly_fields = ("title", "category", "room", "start_time", "length", "end_time")
    extra = 0
    show_change_link = True


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ("event", "name", "public")
    list_filter = ("event",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("event", "name")
    list_filter = ("event",)
    actions = (activate_selected_items, deactivate_selected_items)


@admin.register(ViewRoom)
class ViewRoomAdmin(admin.ModelAdmin):
    list_display = ("admin_get_event", "view", "room", "order")
    list_filter = ("view__event",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("admin_get_event", "title", "personnel_class")
    list_filter = ("personnel_class__event",)
    raw_id_fields = ("personnel_class",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("event", "title", "public")
    list_filter = ("event",)
    inlines = [ProgrammeInline]


@admin.register(SpecialStartTime)
class SpecialStartTimeAdmin(admin.ModelAdmin):
    list_display = ("event", "start_time")
    list_filter = ("event",)


@admin.register(TimeBlock)
class TimeBlockAdmin(admin.ModelAdmin):
    list_display = ("event", "start_time", "end_time")
    list_filter = ("event",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("event", "title")
    list_filter = ("event",)


@admin.register(FreeformOrganizerAdminProxy)
class FreeformOrganizerAdmin(admin.ModelAdmin):
    list_display = ("admin_get_event", "admin_get_title", "text")
    list_filter = ("programme__category__event",)
    raw_id_fields = ("programme",)


@admin.action(description=_("Hide selected feedback"))
def hide_selected_feedback(modeladmin, request, queryset):
    t = now()
    queryset.update(hidden_at=t, hidden_by=request.user)


@admin.action(description=_("Restore selected feedback"))
def restore_selected_feedback(modeladmin, request, queryset):
    queryset.update(hidden_at=None, hidden_by=None)


class ProgrammeFeedbackAdminForm(forms.ModelForm):
    is_visible = forms.BooleanField(
        label=_("Visible"),
        help_text=_("By clearing this tick box you can hide an abusive comment from the site."),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["is_visible"].initial = self.instance.is_visible

    class Meta:
        model = ProgrammeFeedback
        fields = ()


@admin.register(ProgrammeFeedback)
class ProgrammeFeedbackAdmin(admin.ModelAdmin):
    model = ProgrammeFeedback
    form = ProgrammeFeedbackAdminForm
    list_display = (
        "admin_get_event",
        "admin_get_programme_title",
        "author",
        "admin_get_abridged_feedback",
        "admin_is_visible",
    )
    list_filter = ("programme__category__event",)
    readonly_fields = (
        "programme",
        "author",
        "author_ip_address",
        "author_external_username",
        "feedback",
        "is_anonymous",
        "hidden_at",
        "hidden_by",
    )
    actions = [hide_selected_feedback, restore_selected_feedback]

    fieldsets = (
        (
            _("Feedback"),
            dict(
                fields=("programme", "feedback"),
            ),
        ),
        (
            _("Author"),
            dict(
                fields=("author", "author_ip_address", "is_anonymous"),
            ),
        ),
        (
            _("Moderation"),
            dict(
                fields=("is_visible", "hidden_at", "hidden_by"),
            ),
        ),
    )  # type: ignore

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions["delete_selected"]
        return actions

    def save_model(self, request, obj, form, change):
        feedback = obj
        is_visible = form.cleaned_data["is_visible"]

        if is_visible and not feedback.is_visible:
            feedback.hidden_at = None
            feedback.hidden_by = None
            feedback.save()
        elif not is_visible and feedback.is_visible:
            feedback.hidden_at = now()
            feedback.hidden_by = request.user
            feedback.save()


@admin.register(AlternativeProgrammeForm)
class AlternativeProgrammeFormAdmin(admin.ModelAdmin):
    model = AlternativeProgrammeForm
    list_display = ("event", "title", "is_active")
    list_filter = ("event",)


@admin.register(SpecialReservation)
class SpecialReservationAdmin(admin.ModelAdmin):
    model = SpecialReservation
    list_display = ("admin_get_event", "program", "description")
    list_filter = ("program__kompassi_programme__category__event",)
    raw_id_fields = ("program", "zone")
