from core.checks import CheckBase, register_check


class WorkersShouldBelongToTheirRespectiveStateGroup(CheckBase):
    def __init__(self, group_name_suffix, predicate_name):
        from django.contrib.auth.models import Group
        self.group_name_suffix = group_name_suffix
        self.should_belong_to_group = lambda signup: getattr(signup, predicate_name)

    def get_objects(self, **opts):
        from .models import Signup
        return Signup.objects.all()

    def check(self, signup, **opts):
        if self.should_belong_to_group(signup):
            group = self.get_group(signup)
            if not signup.person.user.groups.filter(pk=group.pk).exists():
                return group
            else:
                return None

    def fix(self, signup, group, **opts):
        from core.utils import ensure_user_is_member_of_group
        ensure_user_is_member_of_group(signup.person, group)

    @property
    def name(self):
        return "{class_name}({group_name_suffix})".format(
            class_name=self.__class__.__name__,
            group_name_suffix=self.group_name_suffix,
        )

    def get_group(self, signup):
        meta = signup.event.labour_event_meta
        group, unused = meta.get_or_create_group(
            event=signup.event,
            suffix=self.group_name_suffix,
        )
        return group


for group_name_suffix, predicate_name in [
    ('applicants', 'is_active'),
    ('accepted', 'is_accepted'),
]:
    register_check('labour', WorkersShouldBelongToTheirRespectiveStateGroup(group_name_suffix, predicate_name))