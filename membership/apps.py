from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class MembershipAppConfig(AppConfig):
    name = 'membership'
    verbose_name = 'Jäsenrekisteri'

    def ready(self):
        from . import event_log_entry_types  # noqa
