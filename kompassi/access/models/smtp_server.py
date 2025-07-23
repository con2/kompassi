import logging

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from paramiko import RSAKey, SSHClient

logger = logging.getLogger(__name__)


class SMTPServer(models.Model):
    hostname = models.CharField(
        max_length=255,
        verbose_name=_("SMTP server"),
    )

    crypto = models.CharField(
        max_length=5,
        verbose_name=_("encryption"),
        default="tls",
        choices=[("plain", "Ei salausta"), ("ssl", "SSL"), ("tls", "TLS")],
    )

    port = models.IntegerField(
        verbose_name=_("port number"),
        default=587,
    )

    domains = models.ManyToManyField(
        "access.EmailAliasDomain",
        verbose_name=_("domains"),
        related_name="smtp_servers",
    )

    ssh_server = models.CharField(
        max_length=255,
        verbose_name=_("SSH server"),
        blank=True,
        help_text=(
            "If set, whenever the SMTP passwords for this server are changed, Kompassi will SSH to the server "
            "and write the password file on the server."
        ),
    )
    ssh_port = models.IntegerField(default=22)
    ssh_username = models.CharField(max_length=255, blank=True)
    password_file_path_on_server = models.CharField(max_length=255, blank=True)
    trigger_file_path_on_server = models.CharField(max_length=255, blank=True)

    smtp_passwords: models.QuerySet

    def __str__(self):
        return self.hostname

    def get_smtppasswd_file_contents(self):
        lines = [
            f"{smtp_password.person.user.username}:{smtp_password.password_hash}:{smtp_password.person.full_name}"
            for smtp_password in self.smtp_passwords.all()
        ]
        return "\n".join(lines)

    def push_smtppasswd_file(self):
        from ..tasks import smtp_server_push_smtppasswd_file

        smtp_server_push_smtppasswd_file.delay(self.id)  # type: ignore

    def _push_smtppasswd_file(self):
        logger.info("Pushing smtppasswd file for %s", self)

        # do this early in order not to fail while connected
        contents = self.get_smtppasswd_file_contents()

        pkey = RSAKey.from_private_key_file(settings.KOMPASSI_SSH_PRIVATE_KEY_FILE)

        with SSHClient() as client:
            client.load_host_keys(settings.KOMPASSI_SSH_KNOWN_HOSTS_FILE)
            client.connect(
                hostname=self.ssh_server,
                port=self.ssh_port,
                username=self.ssh_username,
                pkey=pkey,
            )

            with client.open_sftp() as sftp_client:
                with sftp_client.file(self.password_file_path_on_server, "w") as output_file:
                    output_file.write(contents.encode("UTF-8"))

                with sftp_client.file(self.trigger_file_path_on_server, "w"):
                    pass

        logger.info("Successfully pushed smtppasswd file for %s", self)

    class Meta:
        verbose_name = _("SMTP server")
        verbose_name_plural = _("SMTP servers")
