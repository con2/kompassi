from kompassi.core.admin_menus import AdminMenuItem
from kompassi.core.utils import url


def membership_admin_menu_items(request, organization):
    members_url = url("membership_admin_members_view", organization.slug)
    members_active = request.path.startswith(members_url)
    members_text = "Jäsenrekisteri"

    term_text = "Toimikauden tiedot"
    current_term = organization.membership_organization_meta.get_current_term()
    base_term_url = url("membership_admin_new_term_view", organization.slug)
    term_active = request.path.startswith(base_term_url)
    if current_term:
        term_notifications = 0
        term_url = url("membership_admin_term_view", organization.slug, current_term.pk)
    else:
        term_notifications = 1
        term_url = base_term_url

    return [
        AdminMenuItem(is_active=members_active, href=members_url, text=members_text),
        AdminMenuItem(is_active=term_active, href=term_url, text=term_text, notifications=term_notifications),
    ]
