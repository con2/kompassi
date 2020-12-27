from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.views.i18n import set_language


handler403 = 'access.views.permission_denied_view'

urlpatterns = [
    url(r'', include('core.urls')),
    url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=False)),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/setlang/?$', set_language, name='set_language'),

]

for app_name in [
    'labour',
    'programme',
    'tickets',
    'payments',
    'api',
    'api_v2',
    'api_v3',
    'badges',
    'access',
    'sms',
    'desuprofile_integration',
    'membership',
    'events.tracon2019',
    'events.traconpaidat2019',
    'enrollment',
    'intra',
    'feedback',
    'surveys',
    'directory',
    'listings',
    'metrics',
]:
    if app_name in settings.INSTALLED_APPS:
        urlpatterns.append(path(r'', include(f'{app_name}.urls')))

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
