from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import *

urlpatterns = patterns('',
    url(r'^events/(?P<event>[a-z0-9-]+)/signup$', labour_signup_view, name='labour_signup_view'),
    url(r'^profile/qualifications$', labour_qualifications_view, name='labour_qualifications_view'),
    url(r'^profile/qualifications/(?P<qualification>[a-z0-9-]+)$', labour_person_qualification_view, name='labour_person_qualification_view'),

    # XXX make these DELETE and POST of labour_person_qualification_view
    url(r'^profile/qualifications/(?P<qualification>[a-z0-9-]+)/delete$', labour_person_disqualify_view, name='labour_person_disqualify_view'),
    url(r'^profile/qualifications/(?P<qualification>[a-z0-9-]+)/add$', labour_person_qualify_view, name='labour_person_qualify_view'),
)
