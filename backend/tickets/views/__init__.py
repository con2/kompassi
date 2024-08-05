from .admin_views import (
    tickets_admin_accommodation_create_view,
    tickets_admin_accommodation_presence_view,
    tickets_admin_accommodation_view,
    tickets_admin_etickets_view,
    tickets_admin_menu_items,
    tickets_admin_order_view,
    tickets_admin_orders_view,
    tickets_admin_pos_view,
    tickets_admin_stats_by_date_view,
    tickets_admin_stats_view,
    tickets_admin_tools_view,
)
from .tickets_admin_export_view import tickets_admin_export_view, tickets_admin_paulig_export_view
from .tickets_admin_export_yearly_statistics_view import tickets_admin_export_yearly_statistics_view
from .tickets_admin_reports_view import tickets_admin_reports_view
from .tickets_v1_5_views import tickets_router_view
from .tickets_v1_views import (
    ALL_PHASES,
    tickets_accommodation_view,
    tickets_address_view,
    tickets_confirm_view,
    tickets_event_box_context,
    tickets_thanks_view,
    tickets_tickets_view,
    tickets_welcome_view,
)
