from django import forms
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group, User

from kompassi.access.admin import InlineAccessOrganizationMetaAdmin
from kompassi.badges.admin import InlineBadgesEventMetaAdmin
from kompassi.intra.admin import InlineIntraEventMetaAdmin
from kompassi.labour.admin import InlineLabourEventMetaAdmin
from kompassi.membership.admin import InlineMembershipOrganizationMetaAdmin
from kompassi.payments.admin import InlinePaymentsOrganizationMetaAdmin
from kompassi.program_v2.admin import InlineProgramV2EventMetaAdmin
from kompassi.tickets_v2.admin import InlineTicketsV2EventMetaAdmin

from .models import CarouselSlide, Event, Organization, Person, Venue


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "homepage_url")
    ordering = ("name",)
    inlines = (
        InlineMembershipOrganizationMetaAdmin,
        InlineAccessOrganizationMetaAdmin,
        InlinePaymentsOrganizationMetaAdmin,
    )


@admin.action(description="Yhdistä valitut henkilöt")
def merge_selected_people(modeladmin, request, queryset):
    if queryset.count() < 2:
        return

    from kompassi.core.merge_people import find_best_candidate, merge_people

    person_to_spare, people_to_merge = find_best_candidate(queryset)
    merge_people(people_to_merge, into=person_to_spare)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic information", {"fields": [("first_name", "surname"), "nick"]}),
        ("Contact information", {"fields": ["email", "phone", "may_send_info"]}),
        ("Official information", {"fields": ["official_first_names", "muncipality"]}),
        ("Display", {"fields": ["preferred_name_display_style", "preferred_badge_name_display_style"]}),
        ("Notes", {"fields": ["notes"]}),
    ]

    list_display = ("surname", "first_name", "nick", "email", "phone", "username")
    search_fields = ("surname", "first_name", "nick", "email", "user__username")
    ordering = ("surname", "first_name", "nick")
    actions = [merge_selected_people]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "venue", "public", "cancelled")
    list_filter = ("organization", "venue", "public", "cancelled")
    search_fields = ("name",)

    inlines = (
        InlineLabourEventMetaAdmin,
        InlineProgramV2EventMetaAdmin,
        InlineTicketsV2EventMetaAdmin,
        InlineBadgesEventMetaAdmin,
        InlineIntraEventMetaAdmin,
    )

    fieldsets = (
        ("Tapahtuman nimi", dict(fields=("name", "name_genitive", "name_illative", "name_inessive", "slug"))),
        (
            "Tapahtuman perustiedot",
            dict(
                fields=(
                    "venue",
                    "start_time",
                    "end_time",
                    "description",
                    "homepage_url",
                    "logo_file",
                    "logo_url",
                    "organization",
                    "public",
                    "cancelled",
                )
            ),
        ),
    )  # type: ignore

    def get_readonly_fields(self, request, obj=None) -> tuple[str, ...]:
        # slug may be edited when creating but not when modifying existing event
        # (breaks urls and kills puppies)
        if obj:
            return (*self.readonly_fields, "slug")

        return tuple(self.readonly_fields)


# http://stackoverflow.com/a/19932127
class GroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        label="Users",
        queryset=User.objects.all().order_by("username"),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("users", is_stacked=False),  # type: ignore
    )

    class Meta:
        model = Group
        exclude = ()
        widgets = {
            "permissions": admin.widgets.FilteredSelectMultiple("permissions", is_stacked=False),  # type: ignore
        }


# http://stackoverflow.com/a/19932127
class MyGroupAdmin(GroupAdmin):
    form = GroupForm

    def save_model(self, request, obj, form, change):
        # save first to obtain id
        super(GroupAdmin, self).save_model(request, obj, form, change)
        obj.user_set.set(form.cleaned_data["users"], clear=True)  # type: ignore

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields["users"].initial = [o.pk for o in obj.user_set.all()]
        else:
            self.form.base_fields["users"].initial = []
        return GroupForm


admin.site.register(Venue)
admin.site.register(CarouselSlide)


# override GroupAdmin for users of group support in admin
admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
