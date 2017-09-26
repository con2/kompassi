from django.conf.urls import url

from .views import (
    enrollment_admin_special_diets_view,
    enrollment_admin_view,
    enrollment_enroll_view,
    enrollment_list_view,
)

urlpatterns = [
    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/enrollment/?$',
        enrollment_enroll_view,
        name='enrollment_enroll_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/enrollment/list/?$',
        enrollment_list_view,
        name='enrollment_list_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/enrollment/admin/?$',
        enrollment_admin_view,
        name='enrollment_admin_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/enrollment/admin/specialdiets/?$',
        enrollment_admin_special_diets_view,
        name='enrollment_admin_special_diets_view'
    ),
]
