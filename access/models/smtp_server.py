import logging

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from paramiko import SSHClient, RSAKey


logger = logging.getLogger('kompassi')


class SMTPServer(models.Model):
    hostname = models.CharField(
        max_length=255,
        verbose_name=_('SMTP server'),
    )

    crypto = models.CharField(
        max_length=5,
        verbose_name=_('encryption'),
        default='tls',
        choices=[('plain', 'Ei salausta'), ('ssl', 'SSL'), ('tls', 'TLS')],
    )

    port = models.IntegerField(
        verbose_name=_('port number'),
        default=587,
    )

    domains = models.ManyToManyField('access.EmailAliasDomain',
        verbose_name=_('domains'),
        related_name='smtp_servers',
    )

    def __str__(self):
        return self.hostname

    def get_smtppasswd_file_contents(self):
        lines = []

        for smtp_password in self.smtp_passwords.all():
            lines.append('{username}:{password_hash}:{full_name}'.format(
                username=smtp_password.person.user.username,
                password_hash=smtp_password.password_hash,
                full_name=smtp_password.person.full_name,
            ))

        return '\n'.join(lines)

    def push_smtppasswd_file(self):
        if not hasattr(settings, 'KOMPASSI_SMTP_SSH_SERVER'):
            logger.warning('KOMPASSI_SMTP_SSH_SERVER not set, not pushing smtppaswd file for %s', self)
            return

        if 'background_tasks' in settings.INSTALLED_APPS:
            from ..tasks import smtp_server_push_smtppasswd_file
            smtp_server_push_smtppasswd_file.delay(self.id)
        else:
            self._push_smtppaswd_file()

    def _push_smtppasswd_file(self):
        logger.info('Pushing smtppasswd file for %s', self)

        # do this early in order not to fail while connected
        contents = self.get_smtppasswd_file_contents()

        with SSHClient() as client:
            client.load_host_keys(settings.KOMPASSI_SMTP_SSH_KNOWN_HOSTS_FILE)
            client.connect(
                hostname=settings.KOMPASSI_SMTP_SSH_SERVER,
                port=settings.KOMPASSI_SMTP_SSH_PORT,
                username=settings.KOMPASSI_SMTP_SSH_USERNAME,
                pkey=RSAKey.from_private_key_file(settings.KOMPASSI_SMTP_SSH_PRIVATE_KEY_FILE),
            )

            with client.open_sftp() as sftp_client:
                with sftp_client.file(settings.KOMPASSI_SMTP_PASSWORD_FILE, 'w') as output_file:
                    output_file.write(contents.encode('UTF-8'))

                with sftp_client.file(settings.KOMPASSI_SMTP_TRIGGER_FILE, 'w') as trigger_file:
                    pass

        logger.info('Successfully pushed smtppasswd file for %s', self)

    class Meta:
        verbose_name = _('SMTP server')
        verbose_name_plural = _('SMTP servers')
