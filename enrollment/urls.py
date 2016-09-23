from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from .views import (
    enrollment_enroll_view,
)

urlpatterns = [
    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/enrollment/?$',
        enrollment_enroll_view,
        name='enrollment_enroll_view'
    ),

]
