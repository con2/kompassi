from django.conf.urls import url

from .views import feedback_view


urlpatterns = [
    url(
        r'^feedback$',
        feedback_view,
        name='feedback_view',
    )
]
