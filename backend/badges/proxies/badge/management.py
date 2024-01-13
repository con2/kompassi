from ...models import Badge


class BadgeManagementProxy(Badge):
    """
    Contains extra methods for Badge used by the management views.
    """

    @property
    def can_revoke(self):
        """
        Whether or not this badge can be revoked from the badge management UI. Badges created automatically
        via the programme or labour management systems should be revoked there, because if they are revoked
        at the badge management UI, programme/labour systems will just re-create them at will.
        """
        return self.person is None

    @property
    def can_unrevoke(self):
        return self.can_revoke

    class Meta:
        proxy = True
