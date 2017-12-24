from django.conf.urls import url
from django.views.generic import TemplateView

from .views import feedback_view


urlpatterns = [
    url(
        r'^feedback$',
        feedback_view,
        name='feedback_view',
    ),

    url(
        r'^feedback.js$',
        TemplateView.as_view(template_name='feedback.js'),
        name='feedback_js_view',
    )
]
