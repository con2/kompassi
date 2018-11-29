import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import get_code


logger = logging.getLogger('kompassi')


class EmailAliasType(models.Model):
    domain = models.ForeignKey('access.EmailAliasDomain', on_delete=models.CASCADE, verbose_name=_('domain'))
    metavar = models.CharField(
        max_length=255,
        default=_('firstname.lastname'),
        verbose_name=_('metavar'),
        help_text=_('eg. firstname.lastname'),
    )
    account_name_code = models.CharField(max_length=255, default='access.email_aliases:firstname_surname')

    priority = models.IntegerField(
        default=0,
        verbose_name=_('priority'),
        help_text=_(
            'When determining the e-mail address of a person in relation to a specific event, the '
            'e-mail alias type with the smallest priority number wins.'
        ),
    )

    def _make_account_name_for_person(self, person):
        account_name_func = get_code(self.account_name_code)
        return account_name_func(person)

    @classmethod
    def get_or_create_dummy(cls, **kwargs):
        from .email_alias_domain import EmailAliasDomain
        domain, unused = EmailAliasDomain.get_or_create_dummy()
        return cls.objects.get_or_create(domain=domain, **kwargs)

    def admin_get_organization(self):
        return self.domain.organization if self.domain else None
    admin_get_organization.short_description = _('organization')
    admin_get_organization.admin_order_field = 'domain__organization'

    def __str__(self):
        return '{metavar}@{domain}'.format(
            metavar=self.metavar,
            domain=self.domain.domain_name if self.domain else None,
        )

    def create_alias_for_person(self, person, group_grant=None):
        from .email_alias import EmailAlias

        domain_name = self.domain.domain_name

        existing = EmailAlias.objects.filter(person=person, type=self).first()
        if existing:
            logger.debug('Email alias of type %s already exists for %s',
                self,
                person,
            )
            return existing

        account_name = self._make_account_name_for_person(person)
        if account_name:
            email_address = '{account_name}@{domain_name}'.format(
                account_name=account_name,
                domain_name=domain_name,
            )

            existing = EmailAlias.objects.filter(email_address=email_address).first()
            if existing:
                logger.warning('Cross-type collision on email alias %s on type %s for %s',
                    email_address,
                    self,
                    person,
                )
                return existing

            if person.email == email_address:
                logger.warning('Cannot grant alias %s because user %s has it as their email',
                    email_address,
                    person,
                )
                return None

            logger.info('Granting email alias %s of type %s to %s',
                email_address,
                self,
                person,
            )

            newly_created = EmailAlias(
                person=person,
                type=self,
                account_name=account_name,
                group_grant=group_grant,
            )

            newly_created.save()
            return newly_created
        else:
            logger.warn('Not creating alias of type %s for %s (account name generator said None)',
                self,
                person,
            )


    class Meta:
        verbose_name = _('e-mail alias type')
        verbose_name_plural = _('e-mail alias types')
