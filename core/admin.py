# encoding: utf-8

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import User, Group

from .models import Organization, Event, Person, Venue, CarouselSlide


organization_admin_inlines = []

if 'membership' in settings.INSTALLED_APPS:
    from membership.admin import InlineMembershipOrganizationMetaAdmin
    organization_admin_inlines.append(InlineMembershipOrganizationMetaAdmin)

if 'access' in settings.INSTALLED_APPS:
    from access.admin import InlineAccessOrganizationMetaAdmin
    organization_admin_inlines.append(InlineAccessOrganizationMetaAdmin)


if 'directory' in settings.INSTALLED_APPS:
    from directory.admin import InlineDirectoryOrganizationMetaAdmin
    organization_admin_inlines.append(InlineDirectoryOrganizationMetaAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'homepage_url')
    ordering = ('name',)
    inlines = tuple(organization_admin_inlines)


def merge_selected_people(modeladmin, request, queryset):
    if queryset.count() < 2:
        return

    from core.merge_people import find_best_candidate, merge_people

    person_to_spare, people_to_merge = find_best_candidate(queryset)
    merge_people(people_to_merge, into=person_to_spare)
merge_selected_people.short_description = 'Yhdistä valitut henkilöt'


class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': [('first_name', 'surname'), 'nick']}),
        ('Contact information', {'fields': ['email', 'phone', 'may_send_info']}),
        ('Official information', {'fields': ['official_first_names', 'muncipality']}),
        ('Display', {'fields': ['preferred_name_display_style']}),
        ('Notes', {'fields': ['notes']}),
    ]

    list_display = ('surname', 'first_name', 'nick', 'email', 'phone', 'username')
    search_fields = ('surname', 'first_name', 'nick', 'email', 'user__username')
    ordering = ('surname', 'first_name', 'nick')
    actions = [merge_selected_people]


event_admin_inlines = []

if 'labour' in settings.INSTALLED_APPS:
    from labour.admin import InlineLabourEventMetaAdmin
    event_admin_inlines.append(InlineLabourEventMetaAdmin)

if 'programme' in settings.INSTALLED_APPS:
    from programme.admin import InlineProgrammeEventMetaAdmin
    event_admin_inlines.append(InlineProgrammeEventMetaAdmin)

if 'tickets' in settings.INSTALLED_APPS:
    from tickets.admin import InlineTicketsEventMetaAdmin
    event_admin_inlines.append(InlineTicketsEventMetaAdmin)

if 'payments' in settings.INSTALLED_APPS:
    from payments.admin import InlinePaymentsEventMetaAdmin
    event_admin_inlines.append(InlinePaymentsEventMetaAdmin)

if 'badges' in settings.INSTALLED_APPS:
    from badges.admin import InlineBadgesEventMetaAdmin
    event_admin_inlines.append(InlineBadgesEventMetaAdmin)

if 'enrollment' in settings.INSTALLED_APPS:
    from enrollment.admin import InlineEnrollmentEventMetaAdmin
    event_admin_inlines.append(InlineEnrollmentEventMetaAdmin)

if 'intra' in settings.INSTALLED_APPS:
    from intra.admin import InlineIntraEventMetaAdmin
    event_admin_inlines.append(InlineIntraEventMetaAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'venue')
    list_filter = ('organization', 'venue')
    search_fields = ('name',)

    inlines = tuple(event_admin_inlines)

    fieldsets = (
        ('Tapahtuman nimi', dict(fields=(
            'name',
            'name_genitive',
            'name_illative',
            'name_inessive',
            'slug'
        ))),

        ('Tapahtuman perustiedot', dict(fields=(
            'venue',
            'start_time',
            'end_time',
            'description',
            'homepage_url',
            'logo_file',
            'logo_url',
            'organization',
        ))),
    )

    def get_readonly_fields(self, request, obj=None):
        # slug may be edited when creating but not when modifying existing event
        # (breaks urls and kills puppies)
        if obj:
            return self.readonly_fields + ('slug',)

        return self.readonly_fields


# http://stackoverflow.com/a/19932127
class GroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        label='Users',
        queryset=User.objects.all().order_by('username'),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple(
            "users", is_stacked=False))

    class Meta:
        model = Group
        exclude = ()
        widgets = {
            'permissions': admin.widgets.FilteredSelectMultiple(
                "permissions", is_stacked=False),
        }


# http://stackoverflow.com/a/19932127
class MyGroupAdmin(GroupAdmin):
    form = GroupForm

    def save_model(self, request, obj, form, change):
        # save first to obtain id
        super(GroupAdmin, self).save_model(request, obj, form, change)
        obj.user_set.set(form.cleaned_data['users'], clear=True)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields['users'].initial = [o.pk for o in obj.user_set.all()]
        else:
            self.form.base_fields['users'].initial = []
        return GroupForm


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Venue)
admin.site.register(CarouselSlide)


# override GroupAdmin for users of group support in admin
admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
