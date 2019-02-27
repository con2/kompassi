from django import forms
from django.contrib import admin
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from .models import (
    AlternativeProgrammeForm,
    Category,
    Programme,
    ProgrammeEventMeta,
    ProgrammeFeedback,
    Role,
    Room,
    SpecialStartTime,
    Tag,
    TimeBlock,
    View,
    ViewRoom,
)
from .proxies.freeform_organizer.admin import FreeformOrganizerAdminProxy
from .proxies.invitation.admin import InvitationAdminProxy


def deactivate_selected_items(modeladmin, request, queryset):
    queryset.update(active=False)
deactivate_selected_items.short_description = _('Deactivate selected items')


def activate_selected_items(modeladmin, request, queryset):
    queryset.update(active=False)
activate_selected_items.short_description = _('Activate selected items')


class InlineProgrammeEventMetaAdmin(admin.StackedInline):
    model = ProgrammeEventMeta


class ProgrammeRoleInline(admin.TabularInline):
    model = Programme.organizers.through
    verbose_name = 'organizer'
    verbose_name_plural = 'organizers'


class ProgrammeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': ['title', 'description', 'category', 'tags']}),
        ('Time and location', {'fields': ['room', ('start_time', 'length')]}),
        ('Notes', {'fields': ['notes']}),
    ]

    inlines = [
        ProgrammeRoleInline,
    ]

    list_display = ('title', 'category', 'room', 'start_time', 'length', 'end_time')
    list_filter = ('room', 'start_time', 'category')


class ViewAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'public')
    list_filter = ('event',)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('event', 'name')
    list_filter = ('event',)
    actions = (activate_selected_items, deactivate_selected_items)


class ViewRoomAdmin(admin.ModelAdmin):
    list_display = ('admin_get_event', 'view', 'room', 'order')
    list_filter = ('view__event',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('admin_get_event', 'title', 'personnel_class')
    list_filter = ('personnel_class__event',)
    raw_id_fields = ('personnel_class',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'public')
    list_filter = ('event',)


class SpecialStartTimeAdmin(admin.ModelAdmin):
    list_display = ('event', 'start_time')
    list_filter = ('event',)


class TimeBlockAdmin(admin.ModelAdmin):
    list_display = ('event', 'start_time', 'end_time')
    list_filter = ('event',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('event', 'title')
    list_filter = ('event',)


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('admin_get_event', 'admin_get_title', 'email', 'state', 'created_by')
    list_filter = ('programme__category__event', 'state')
    ordering = ('programme__category__event', 'programme__title', 'email')
    raw_id_fields = ('programme',)


class FreeformOrganizerAdmin(admin.ModelAdmin):
    list_display = ('admin_get_event', 'admin_get_title', 'text')
    list_filter = ('programme__category__event',)
    raw_id_fields = ('programme',)


def hide_selected_feedback(modeladmin, request, queryset):
    t = now()
    queryset.update(hidden_at=t, hidden_by=request.user)
hide_selected_feedback.short_description = _('Hide selected feedback')

def restore_selected_feedback(modeladmin, request, queryset):
    queryset.update(hidden_at=None, hidden_by=None)
restore_selected_feedback.short_description = _('Restore selected feedback')


class ProgrammeFeedbackAdminForm(forms.ModelForm):
    is_visible = forms.BooleanField(label=_('Visible'), help_text=_('By clearing this tick box you can hide an abusive comment from the site.'), required=False)

    def __init__(self, *args, **kwargs):
        super(ProgrammeFeedbackAdminForm, self).__init__(*args, **kwargs)

        self.fields['is_visible'].initial = self.instance.is_visible

    class Meta:
        model = ProgrammeFeedback
        fields = ()


class ProgrammeFeedbackAdmin(admin.ModelAdmin):
    model = ProgrammeFeedback
    form = ProgrammeFeedbackAdminForm
    list_display = ('admin_get_event', 'admin_get_programme_title', 'author', 'admin_get_abridged_feedback', 'admin_is_visible')
    list_filter = ('programme__category__event',)
    readonly_fields = ('programme', 'author', 'author_ip_address', 'feedback', 'is_anonymous', 'hidden_at', 'hidden_by')
    actions = [hide_selected_feedback, restore_selected_feedback]

    fieldsets = (
        (_('Feedback'), dict(
            fields=('programme', 'feedback'),
        )),
        (_('Author'), dict(
            fields=('author', 'author_ip_address', 'is_anonymous'),
        )),
        (_('Moderation'), dict(
            fields=('is_visible', 'hidden_at', 'hidden_by'),
        ))
    )

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def get_actions(self, request):
        actions = super(ProgrammeFeedbackAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        feedback = obj
        is_visible = form.cleaned_data['is_visible']

        if is_visible and not feedback.is_visible:
            feedback.hidden_at = None
            feedback.hidden_by = None
            feedback.save()
        elif not is_visible and feedback.is_visible:
            feedback.hidden_at = now()
            feedback.hidden_by = request.user
            feedback.save()


class AlternativeProgrammeFormAdmin(admin.ModelAdmin):
    model = AlternativeProgrammeForm
    list_display = ('event', 'title', 'is_active')
    list_filter = ('event',)


admin.site.register(AlternativeProgrammeForm, AlternativeProgrammeFormAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FreeformOrganizerAdminProxy, FreeformOrganizerAdmin)
admin.site.register(InvitationAdminProxy, InvitationAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(ProgrammeFeedback, ProgrammeFeedbackAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(SpecialStartTime, SpecialStartTimeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TimeBlock, TimeBlockAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(ViewRoom, ViewRoomAdmin)
