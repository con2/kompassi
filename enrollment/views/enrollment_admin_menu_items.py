# encoding: utf-8

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from core.utils import url
from core.admin_menus import AdminMenuItem


def enrollment_admin_menu_items(request, event):
    enrolled_url = url('enrollment_admin_view', event.slug)
    enrolled_active = request.path == enrolled_url
    enrolled_text = _('Enrolled people')

    special_diets_url = url('enrollment_admin_special_diets_view', event.slug)
    special_diets_active = request.path == special_diets_url
    special_diets_text = _('Special diets')

    return [
        AdminMenuItem(is_active=enrolled_active, href=enrolled_url, text=enrolled_text),
        AdminMenuItem(is_active=special_diets_active, href=special_diets_url, text=special_diets_text),
    ]
