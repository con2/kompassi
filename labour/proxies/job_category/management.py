from ...models import JobCategory


class JobCategoryManagementProxy(JobCategory):
    """
    Extra methods for JobCategory used only by management views.
    """

    @property
    def show_remove_button(self):
        return self.pk is not None

    @property
    def can_remove(self):
        return self.pk is not None and not self.signup_set.exists()

    class Meta:
        proxy = True
