from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from passlib.hash import md5_crypt

from ..utils import generate_machine_password


class SMTPPassword(models.Model):
    smtp_server = models.ForeignKey(
        "access.SMTPServer",
        on_delete=models.CASCADE,
        related_name="smtp_passwords",
        verbose_name=_("SMTP server"),
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        related_name="smtp_passwords",
        verbose_name=_("person"),
    )

    password_hash = models.CharField(
        max_length=255,
        verbose_name=_("password hash"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    @classmethod
    def create_for_domain_and_person(cls, domain, person, hash_module=md5_crypt):
        smtp_server = domain.smtp_servers.first()
        pw = generate_machine_password()

        with transaction.atomic():
            cls.objects.filter(smtp_server=smtp_server, person=person).delete()
            obj = cls(smtp_server=smtp_server, person=person, password_hash=hash_module.encrypt(pw))
            obj.save()

        if smtp_server.ssh_server:
            smtp_server.push_smtppasswd_file()

        return pw, obj

    def as_dict(self):
        return dict(
            username=self.person.user.username,
            password_hash=self.password_hash,
        )

    class Meta:
        verbose_name = _("SMTP password")
        verbose_name_plural = _("SMTP passwords")
