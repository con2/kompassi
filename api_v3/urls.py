from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from core.views.api_v3_views import EventViewSet
from forms.views.api_v3_views import FormViewSet, FormResponseViewSet

from .views import CurrentUserView
from .utils import OptionalTrailingSlashRouter


# Create a router and register our viewsets with it.
router = OptionalTrailingSlashRouter()
router.register(r'events', EventViewSet)
router.register(r'forms', FormViewSet)

forms_router = NestedSimpleRouter(router, 'forms', lookup='form')
forms_router.register(r'responses', FormResponseViewSet, base_name='form-response')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    re_path(r'^api/v3/user/?$', CurrentUserView.as_view(), name='api_v3_current_user_view'),
    path('api/v3/', include(router.urls)),
    path('api/v3/', include(forms_router.urls)),
]
