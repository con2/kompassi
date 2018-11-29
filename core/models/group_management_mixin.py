# encoding: utf-8

from django.conf import settings

from ..utils import ensure_groups_exist


class GroupManagementMixin(object):
    @staticmethod
    def is_user_in_group(user, group):
        if not user.is_authenticated:
            return False

        return user.groups.filter(pk=group.pk).exists()

    def is_user_in_admin_group(self, user):
        return self.is_user_in_group(user, self.admin_group)

    def is_user_admin(self, user):
        return user.is_superuser or self.is_user_in_admin_group(user)

    @classmethod
    def make_group_name(cls, host, suffix):
        # to avoid cases where someone calls .get_or_create_groups(foo, 'admins')
        # and would otherwise get groups a, d, m, i, n, s...
        assert isinstance(suffix, str) and len(suffix) > 1

        from django.contrib.contenttypes.models import ContentType

        ctype = ContentType.objects.get_for_model(cls)

        return '{installation_slug}-{host_slug}-{app_label}-{suffix}'.format(
            installation_slug=settings.KOMPASSI_INSTALLATION_SLUG,
            host_slug=host.slug,
            app_label=ctype.app_label,
            suffix=suffix,
        )

    @classmethod
    def get_or_create_groups(cls, host, suffixes):
        group_names = [cls.make_group_name(host, suffix) for suffix in suffixes]

        return ensure_groups_exist(group_names)
