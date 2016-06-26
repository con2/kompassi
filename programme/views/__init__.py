from .public_views import (
    programme_event_box_context,
    programme_internal_adobe_taggedtext_view,
    programme_internal_timetable_view,
    programme_json_view,
    programme_mobile_timetable_view,
    programme_profile_menu_items,
    programme_special_view,
    programme_timetable_view,
)

from .admin_views import (
    programme_admin_create_view,
    programme_admin_email_list_view,
    programme_admin_timetable_view,
    programme_admin_view,
    programme_admin_email_list_view,
    programme_admin_special_view,
)


from .programme_admin_detail_view import (
    programme_admin_change_host_role_view,
    programme_admin_change_invitation_role_view,
    programme_admin_detail_view,
)

from .programme_accept_invitation_view import programme_accept_invitation_view
from .programme_admin_invitations_view import programme_admin_invitations_view
from .programme_admin_menu_items import programme_admin_menu_items
from .programme_admin_publish_view import programme_admin_publish_view
from .programme_profile_detail_view import programme_profile_detail_view
from .programme_profile_view import programme_profile_view
