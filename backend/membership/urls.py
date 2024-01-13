from django.urls import re_path

from .views import (
    membership_admin_emails_api,
    membership_admin_member_view,
    membership_admin_members_view,
    membership_admin_term_view,
    membership_apply_view,
    membership_pay_fee_view,
    membership_profile_view,
)

urlpatterns = [
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/apply/?$",
        membership_apply_view,
        name="membership_apply_view",
    ),
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/admin/members/?$",
        membership_admin_members_view,
        kwargs=dict(format="screen"),
        name="membership_admin_members_view",
    ),
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/admin/members.(?P<format>html|xlsx|csv)/?$",
        membership_admin_members_view,
        name="membership_admin_export_view",
    ),
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/admin/members/(?P<person_id>[0-9]+)/?$",
        membership_admin_member_view,
        name="membership_admin_member_view",
    ),
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/admin/term/(?P<term_id>\d+)/?$",
        membership_admin_term_view,
        name="membership_admin_term_view",
    ),
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/admin/term/?$",
        membership_admin_term_view,
        name="membership_admin_new_term_view",
    ),
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/fee/?$",
        membership_pay_fee_view,
        name="membership_pay_fee_view",
    ),
    re_path(r"^profile/organizations/?$", membership_profile_view, name="membership_profile_view"),
    re_path(
        r"^api/v1/organizations/(?P<organization_slug>[a-z0-9-]+)/members/emails.txt$",
        membership_admin_emails_api,
        name="membership_admin_emails_api",
    ),
]
