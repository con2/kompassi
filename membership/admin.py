from django.contrib import admin

from .models import MembershipOrganizationMeta, Membership


class InlineMembershipOrganizationMetaAdmin(admin.StackedInline):
    model = MembershipOrganizationMeta


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('organization', 'person')
    list_filter = ('organization',)
    raw_id_fields = ('person',)


admin.site.register(Membership, MembershipAdmin)
