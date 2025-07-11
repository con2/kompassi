from django.urls import re_path
from django.views.generic import RedirectView

from programme.views.paikkala_views import paikkala_special_reservation_view

from .views.admin_detail_view import admin_detail_view
from .views.admin_feedback_view import admin_feedback_view
from .views.admin_mail_editor_view import admin_mail_editor_view
from .views.admin_mail_view import admin_mail_view
from .views.admin_organizers_view import admin_organizers_view
from .views.admin_reservation_status_view import admin_reservation_status_view
from .views.admin_reservations_export_view import admin_reservations_export_view
from .views.admin_rooms_view import admin_rooms_view
from .views.admin_views import admin_email_list_view, admin_view
from .views.paikkala_views import paikkala_inspection_view, paikkala_relinquish_view, paikkala_reservation_view
from .views.profile_detail_view import profile_detail_view
from .views.profile_feedback_view import profile_feedback_view
from .views.profile_reservations_view import profile_reservations_view
from .views.profile_view import profile_view
from .views.schedule_redirect_view import schedule_redirect_view

app_name = "programme"
urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/timetable(?P<suffix>.*)",
        RedirectView.as_view(url="/events/%(event_slug)s/programme%(suffix)s", permanent=False),
        name="programme_old_urls_redirect",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/?$",
        schedule_redirect_view,
        name="schedule_redirect_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/special/?$",
        schedule_redirect_view,
        name="schedule_redirect_view_special",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/(?P<programme_id>\d+)/reservations/(?P<pk>\d+)/relinquish/?$",
        paikkala_relinquish_view,
        name="paikkala_relinquish_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/(?P<programme_id>\d+)/reservations/(?P<pk>\d+)/inspect/(?P<key>.+?)/?$",
        paikkala_inspection_view,
        name="paikkala_inspection_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/(?P<programme_id>\d+)/reservations/?$",
        paikkala_reservation_view,
        name="paikkala_reservation_view",
    ),
    re_path(
        r"^reservations/(?P<code>[a-z0-9-]+)/?$",
        paikkala_special_reservation_view,
        name="paikkala_special_reservation_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/?$",
        admin_view,
        name="admin_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/(?P<programme_id>\d+)/?$",
        admin_detail_view,
        name="admin_detail_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/(?P<programme_id>\d+)/reservations\.xlsx$",
        admin_reservations_export_view,
        name="admin_reservations_export_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/feedback/?$",
        admin_feedback_view,
        name="admin_feedback_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/organizers/?$",
        admin_organizers_view,
        name="admin_organizers_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/organizers\.(?P<format>\w+)?$",
        admin_organizers_view,
        name="admin_export_organizers_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/rooms/?$",
        admin_rooms_view,
        name="admin_rooms_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/reservations/?$",
        admin_reservation_status_view,
        name="admin_reservation_status_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/programme\.(?P<format>xlsx|csv|tsv|html)$",
        admin_view,
        name="admin_export_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/emails\.txt$",
        admin_email_list_view,
        name="admin_email_list_view",
    ),
    re_path(r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/mail/?$", admin_mail_view, name="admin_mail_view"),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/mail/new/?$",
        admin_mail_editor_view,
        name="admin_mail_new_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/programme/admin/mail/(?P<message_id>\d+)/?$",
        admin_mail_editor_view,
        name="admin_mail_editor_view",
    ),
    re_path(
        r"^profile/programmes/?$",
        profile_view,
        name="profile_view",
    ),
    re_path(
        r"^profile/programmes/(?P<programme_id>\d+)/?$",
        profile_detail_view,
        name="profile_detail_view",
    ),
    re_path(
        r"^profile/programmes/(?P<programme_id>\d+)/feedback/?$",
        profile_feedback_view,
        name="profile_feedback_view",
    ),
    re_path(
        r"^profile/reservations/?",
        profile_reservations_view,
        name="profile_reservations_view",
    ),
]
