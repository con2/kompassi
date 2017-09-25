from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.timezone import now


METHOD_CHOICES = [
    ('GET', 'GET'),
    ('POST', 'POST'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE'),
]


class ACLEntry(models.Model):
    group = models.ForeignKey('auth.Group', blank=True, null=True)
    user = models.Foreignkey(settings.AUTH_USER_MODEL, blank=True, null=True)

    path = models.CharField(max_length=512)
    method = models.CharField(
        max_length=max(len(key) for (key, value) in METHOD_CHOICES),
        default='GET',
    )

    active_from = models.DateTimeField(blank=True, null=True)
    active_until = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = [('path', 'method', 'active_from', 'active_until')]

    @classmethod
    def get_entries(cls, request, t=None, **extra_criteria):
        """
        Returns ACL entries that match the given request.

        NOTE: The caller is responsible for running .distinct() on the results,
        because they might just as well care only for the existence.
        """

        if t is None:
            t = now()

        q = Q(
            path=request.path,
            method=request.method,
            active_from__lte=t,
            **extra_criteria
        )

        q &= Q(active_until__gt=t) | Q(active_until__isnull=True)

        if request.user.is_anonymous():
            q &= Q(
                group__isnull=True,
                user__isnull=True,
            )
        else:
            q &= Q(user=request.user) | Q(group__in=request.user.group_set.all())

        return cls.objects.filter(q)

    @classmethod
    def is_allowed(cls, request, t=None):
        return cls.get_entries(request, t=t).exists()
