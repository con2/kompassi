from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

def if_installed(appname, *args, **kwargs):
    ret = url(*args, **kwargs)
    if appname not in settings.INSTALLED_APPS:
        ret.resolve = lambda *args: None
    return ret

urlpatterns = patterns('',
    url(r'', include('core.urls')),
    if_installed('labour', r'', include('labour.urls')),
    if_installed('programme', r'', include('programme.urls')),
    url(r'^admin/', include(admin.site.urls)),
)