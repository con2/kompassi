from django.conf import settings

from ..utils import ensure_groups_exist


class GroupManagementMixin:
    @staticmethod
    def is_user_in_group(user, group):
        if not user.is_authenticated:
            return False

        return user.groups.filter(pk=group.pk).exists()

    def is_user_in_admin_group(self, user):
        return self.is_user_in_group(user, self.admin_group)

    # DEPRECATED: Once all applications have moved to CBAC, remove this
    def is_user_admin(self, user):
        return user.is_superuser or self.is_user_in_admin_group(user)

    @classmethod
    def make_group_name(cls, host, suffix):
        # to avoid cases where someone calls .get_or_create_groups(foo, 'admins')
        # and would otherwise get groups a, d, m, i, n, s...
        if not isinstance(suffix, str):
            raise TypeError("suffix must be a string")
        if len(suffix) <= 1:
            raise ValueError(f"suffix {suffix!r} should be longer than a single character")

        from django.contrib.contenttypes.models import ContentType

        ctype = ContentType.objects.get_for_model(cls)

        return f"{settings.KOMPASSI_INSTALLATION_SLUG}-{host.slug}-{ctype.app_label}-{suffix}"

    @classmethod
    def get_or_create_groups(cls, host, suffixes):
        group_names = [cls.make_group_name(host, suffix) for suffix in suffixes]

        return ensure_groups_exist(group_names)
