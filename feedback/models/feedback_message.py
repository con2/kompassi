# encoding: utf-8



from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatewords


class FeedbackMessage(models.Model):
    context = models.CharField(max_length=1024, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    author_ip_address = models.CharField(
        max_length=48,
        blank=True,
        default='',
        verbose_name=_('IP address'),
    )

    feedback = models.TextField(verbose_name=_('feedback'))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('feedback message')
        verbose_name_plural = _('feedback messages')

    def admin_get_abridged_feedback(self, num_words=20):
        return truncatewords(self.feedback, num_words)
    admin_get_abridged_feedback.short_description = _('feedback')

    @property
    def author_display_name(self):
        from core.models import Person

        if self.author:
            try:
                return self.author.person.display_name
            except Person.DoesNotExist:
                return self.author.get_full_name()
        else:
            return 'Anonymous ({ip_address})'.format(ip_address=self.author_ip_address)

    @property
    def author_email(self):
        return self.author.email if self.author else ''
