from django.contrib import admin

from .models import MembershipOrganizationMeta, Membership


class InlineMembershipOrganizationMetaAdmin(admin.StackedInline):
    model = MembershipOrganizationMeta


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('organization', 'person')
    list_filter = ('organization',)
    search_fields = (
        'person__surname',
        'person__first_name',
        'person__official_first_names',
        'person__nick',
        'person__email',
    )
    raw_id_fields = ('person',)


admin.site.register(Membership, MembershipAdmin)
