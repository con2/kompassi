from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import labour_wiki_page_view

urlpatterns = patterns('',
    url(r'^events/(?P<event>[a-z0-9-]+)/wikis/(?P<space>[a-z0-9-]+)$', labour_wiki_page_view, name='labour_wiki_frontpage_view'),
    url(r'^events/(?P<event>[a-z0-9-]+)/wikis/(?P<space>[a-z0-9-]+)/(?P<page>[a-z0-9/-]+)$', labour_wiki_page_view, name='labour_wiki_page_view'),
    url(r'^events/(?P<event>[a-z0-9-]+)/wikis/(?P<space>[a-z0-9-]+)/(?P<page>[a-z0-9/-]+)/edit$', labour_wiki_edit_view, name='labour_wiki_edit_view'),
)
