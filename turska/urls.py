from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

actual_patterns = [
    url(r'', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

for app_name in [
    'labour',
    'programme',
    'tickets',
    'payments',
    'atlassian_integration',
    'api',
]:
    if app_name in settings.INSTALLED_APPS:
        actual_patterns.append(url(r'', include('{app_name}.urls'.format(app_name=app_name))))

urlpatterns = patterns('', *actual_patterns)
