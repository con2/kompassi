from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


actual_patterns = [
    url(r'', include('core.urls')),
    url(r'^admin$', RedirectView.as_view(url='/admin/')),
    url(r'^admin/', include(admin.site.urls)),
]

for app_name in [
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
]:
    if app_name in settings.INSTALLED_APPS:
        actual_patterns.append(url(r'', include('{app_name}.urls'.format(app_name=app_name))))

urlpatterns = patterns('', *actual_patterns)
