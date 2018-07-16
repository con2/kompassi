from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.i18n import set_language


urlpatterns = [
    url(r'', include('core.urls')),
    url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=False)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/setlang/?$', set_language, name='set_language'),

]

for app_name in [
    'django_prometheus',
    'labour',
    'programme',
    'tickets',
    'payments',
    'api',
    'api_v2',
    'badges',
    'access',
    'nexmo',
    'sms',
    'desuprofile_integration',
    'membership',
    'events.tracon2017',
    'enrollment',
    'intra',
    'feedback',
    'surveys',
    'directory',
    'listings',
]:
    if app_name in settings.INSTALLED_APPS:
        urlpatterns.append(url(r'', include('{app_name}.urls'.format(app_name=app_name))))
