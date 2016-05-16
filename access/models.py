# encoding: utf-8

import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.utils.timezone import now

import requests
from requests.exceptions import HTTPError
from passlib.hash import md5_crypt

from core.utils import get_code, SLUG_FIELD_PARAMS
from core.models import Person, Event, Organization, GroupManagementMixin

from .utils import generate_machine_password


logger = logging.getLogger('kompassi')

STATE_CHOICES = [
    ('pending', u'Odottaa hyväksyntää'),
    ('approved', u'Hyväksytty, odottaa toteutusta'),
    ('granted', u'Myönnetty'),
    ('rejected', u'Hylätty'),
]
STATE_CSS = dict(
    pending='label-warning',
    approved='label-primary',
    granted='label-success',
    rejected='label-danger',
)


class AccessOrganizationMeta(models.Model, GroupManagementMixin):
    organization = models.OneToOneField(Organization, primary_key=True, verbose_name=u'Organisaatio')
    admin_group = models.ForeignKey(Group, verbose_name=u'Ylläpitäjäryhmä')

    def __unicode__(self):
        return self.organization.name if self.organization is not None else u'None'

    class Meta:
        verbose_name = u'Pääsynvalvonnan asetukset'
        verbose_name = u'Pääsynvalvonnan asetukset'

    def get_group(self, suffix):
        group_name = self.make_group_name(self.organization, suffix)
        return Group.objects.get(name=group_name)


class Privilege(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    disclaimers = models.TextField(blank=True)
    request_success_message = models.TextField(blank=True)

    grant_code = models.CharField(max_length=256)

    def grant(self, person):
        gp, created = GrantedPrivilege.objects.get_or_create(
            privilege=self,
            person=person,
            defaults=dict(
                state='approved'
            )
        )

        if gp.state != 'approved':
            return

        if 'background_tasks' in settings.INSTALLED_APPS:
            from .tasks import grant_privilege
            grant_privilege.delay(self.pk, person.pk)
        else:
            self._grant(person)

    def _grant(self, person):
        gp = GrantedPrivilege.objects.get(privilege=self, person=person, state='approved')

        grant_function = get_code(self.grant_code)
        grant_function(self, person)

        gp.state = 'granted'
        gp.save()

    @classmethod
    def get_potential_privileges(cls, person, **extra_criteria):
        assert person.user is not None
        return cls.objects.filter(
            group_privileges__group__in=person.user.groups.all(),
            **extra_criteria
        ).exclude(granted_privileges__person=person).distinct()

    def get_absolute_url(self):
        return u'{base_url}#privilege-{id}'.format(
            base_url=reverse('access_profile_privileges_view'),
            id=self.id,
        )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Käyttöoikeus'
        verbose_name_plural = u'Käyttöoikeudet'


class GroupPrivilege(models.Model):
    privilege = models.ForeignKey(Privilege, related_name='group_privileges')
    group = models.ForeignKey(Group, related_name='group_privileges')
    event = models.ForeignKey(Event, null=True, blank=True, related_name='group_privileges')

    def __unicode__(self):
        return u'{group_name} - {privilege_title}'.format(
            group_name=self.group.name if self.group else None,
            privilege_title=self.privilege.title if self.privilege else None,
        )

    class Meta:
        verbose_name = u'Ryhmän käyttöoikeus'
        verbose_name_plural = u'Ryhmien käyttöoikeudet'

        unique_together = [('privilege', 'group')]


class GrantedPrivilege(models.Model):
    privilege = models.ForeignKey(Privilege, related_name='granted_privileges')
    person = models.ForeignKey(Person, related_name='granted_privileges')
    state = models.CharField(default='granted', max_length=8, choices=STATE_CHOICES)

    granted_at = models.DateTimeField(auto_now_add=True)

    @property
    def state_css(self):
        return STATE_CSS[self.state]

    def __unicode__(self):
        return u'{person_name} - {privilege_title}'.format(
            person_name=self.person.full_name if self.person else None,
            privilege_title=self.privilege.title if self.privilege else None,
        )

    class Meta:
        verbose_name = u'Myönnetty käyttöoikeus'
        verbose_name_plural = u'Myönnetyt käyttöoikeudet'

        unique_together = [('privilege', 'person')]


class SlackError(RuntimeError):
    pass


class SlackAccess(models.Model):
    privilege = models.OneToOneField(Privilege, related_name='slack_access')
    team_name = models.CharField(max_length=255, verbose_name=u'Slack-yhteisön nimi')
    api_token = models.CharField(max_length=255, default=u'test', verbose_name=u'API-koodi')

    @property
    def invite_url(self):
        return 'https://{team_name}.slack.com/api/users.admin.invite'.format(team_name=self.team_name)

    def grant(self, person):
        if self.api_token == 'test':
            logger.warn(u'Using test mode for SlackAccess Privileges. No invites are actually being sent. '
                u'Would invite {name_and_email} to Slack if an actual API token were set.'.format(
                    name_and_email=person.name_and_email,
                )
            )
            return

        try:
            response = requests.get(self.invite_url, params=dict(
                token=self.api_token,
                email=person.email,
                first_name=person.first_name,
                last_name=person.surname,
                set_active=True,
            ))

            response.raise_for_status()
            result = response.json()

            if not result.get('ok'):
                raise SlackError(result)

            return result
        except (HTTPError, KeyError, IndexError, ValueError) as e:
            unused, unused, trace = sys.exc_info()
            raise SlackError(e), None, trace

    class Meta:
        verbose_name = u'Slack-kutsuautomaatti'
        verbose_name_plural = u'Slack-kutsuautomaatit'


class EmailAliasDomain(models.Model):
    domain_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=u'Verkkotunnus',
        help_text=u'Esim. example.com'
    )
    organization = models.ForeignKey(Organization, verbose_name=u'Organisaatio')

    @classmethod
    def get_or_create_dummy(cls, domain_name='example.com'):
        organization, unused = Organization.get_or_create_dummy()

        return cls.objects.get_or_create(domain_name=domain_name, defaults=dict(organization=organization))

    def __unicode__(self):
        return self.domain_name

    class Meta:
        verbose_name = u'Verkkotunnus'
        verbose_name_plural = u'Verkkotunnukset'



class EmailAliasType(models.Model):
    domain = models.ForeignKey(EmailAliasDomain, verbose_name=u'Verkkotunnus')
    metavar = models.CharField(
        max_length=255,
        default=u'etunimi.sukunimi',
        verbose_name=u'Metamuuttuja',
        help_text=u'Esim. "etunimi.sukunimi"',
    )
    account_name_code = models.CharField(max_length=255, default='access.email_aliases:firstname_surname')

    def _make_account_name_for_person(self, person):
        account_name_func = get_code(self.account_name_code)
        return account_name_func(person)

    @classmethod
    def get_or_create_dummy(cls, **kwargs):
        domain, unused = EmailAliasDomain.get_or_create_dummy()
        return cls.objects.get_or_create(domain=domain, **kwargs)

    def admin_get_organization(self):
        return self.domain.organization if self.domain else None
    admin_get_organization.short_description = u'Organisaatio'
    admin_get_organization.admin_order_field = 'domain__organization'

    def __unicode__(self):
        return u'{metavar}@{domain}'.format(
            metavar=self.metavar,
            domain=self.domain.domain_name if self.domain else None,
        )

    def create_alias_for_person(self, person, group_grant=None):
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
        verbose_name = u'Sähköpostialiaksen tyyppi'
        verbose_name_plural = u'Sähköpostialiasten tyypit'


class GroupEmailAliasGrant(models.Model):
    group = models.ForeignKey(Group, verbose_name=u'Ryhmä')
    type = models.ForeignKey(EmailAliasType, verbose_name=u'Tyyppi')
    active_until = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'{group_name}: {type}'.format(
            group_name=self.group.name if self.group else None,
            type=self.type,
        )

    @classmethod
    def ensure_aliases(cls, person, t=None):
        print 'ensure_aliases', person

        if person.user is None:
            logger.warn('Cannot ensure_aliases for Person without User: %s', person.full_name)
            return

        if t is None:
            t = now()

        group_grants = cls.objects.filter(group__in=person.user.groups.all())

        # filter out inactive grants
        group_grants = group_grants.filter(Q(active_until__gt=t) | Q(active_until__isnull=True))

        for group_grant in group_grants:
            group_grant.type.create_alias_for_person(person, group_grant=group_grant)

    def admin_get_organization(self):
        return self.type.domain.organization
    admin_get_organization.short_description = u'Organisaatio'
    admin_get_organization.admin_order_field = 'type__domain__organization'

    class Meta:
        verbose_name = u'Myöntämiskanava'
        verbose_name_plural = u'Myöntämiskanavat'


class EmailAlias(models.Model):
    type = models.ForeignKey(EmailAliasType, verbose_name=u'Tyyppi', related_name='email_aliases')
    person = models.ForeignKey(Person, verbose_name=u'Henkilö', related_name='email_aliases')

    account_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'Tunnus',
        help_text=u'Ennen @-merkkiä tuleva osa sähköpostiosoitetta. Muodostetaan automaattisesti jos tyhjä.',
    )

    # denormalized to facilitate searching etc
    email_address = models.CharField(
        max_length=511,
        verbose_name=u'Sähköpostiosoite',
        help_text=u'Muodostetaan automaattisesti',
    )

    # to facilitate easy pruning of old addresses
    group_grant = models.ForeignKey(GroupEmailAliasGrant,
        blank=True,
        null=True,
        verbose_name=u'Myöntämiskanava',
        help_text=u'Myöntämiskanava antaa kaikille tietyn ryhmän jäsenille tietyntyyppisen sähköpostialiaksen. '
            u'Jos aliakselle on asetettu myöntämiskanava, alias on myönnetty tämän myöntämiskanavan perusteella, '
            u'ja kun myöntämiskanava vanhenee, kaikki sen perusteella myönnetyt aliakset voidaan poistaa kerralla.'
    )

    # denormalized, for unique_together and easy queries
    domain = models.ForeignKey(EmailAliasDomain, verbose_name=u'Verkkotunnus')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Luotu')
    modified_at = models.DateTimeField(auto_now=True, verbose_name=u'Muokattu')

    def _make_email_address(self):
        return u'{account_name}@{domain}'.format(
            account_name=self.account_name,
            domain=self.domain.domain_name,
        ) if self.account_name and self.domain else None

    @classmethod
    def get_or_create_dummy(cls):
        alias_type, unused = EmailAliasType.get_or_create_dummy()
        person, unused = Person.get_or_create_dummy()

        return cls.objects.get_or_create(
            type=alias_type,
            person=person,
        )

    def admin_get_organization(self):
        return self.type.domain.organization if self.type else None
    admin_get_organization.short_description = u'Organisaatio'
    admin_get_organization.admin_order_field = 'type__domain__organization'

    def __unicode__(self):
        return self.email_address

    class Meta:
        verbose_name = u'Sähköpostialias'
        verbose_name_plural = u'Sähköpostialiakset'

        unique_together = [('domain', 'account_name')]


@receiver(pre_save, sender=EmailAlias)
def populate_email_alias_computed_fields(sender, instance, **kwargs):
    if instance.type:
        instance.domain = instance.type.domain

        if instance.person and not instance.account_name:
            instance.account_name = instance.type._make_account_name_for_person(instance.person)

        if instance.account_name:
            instance.email_address = instance._make_email_address()


class SMTPServer(models.Model):
    hostname = models.CharField(
        max_length=255,
        verbose_name=u'SMTP-palvelin',
    )

    crypto = models.CharField(
        max_length=5,
        verbose_name=u'Salaus',
        default='tls',
        choices=[('plain', 'Ei salausta'), ('ssl', 'SSL'), ('tls', 'TLS')],
    )

    port = models.IntegerField(
        verbose_name=u'Porttinumero',
        default=587,
    )

    domains = models.ManyToManyField(EmailAliasDomain, verbose_name=u'Verkkotunnukset', related_name='smtp_servers')

    def __unicode__(self):
        return self.hostname

    class Meta:
        verbose_name = u'SMTP-palvelin'
        verbose_name_plural = u'SMTP-palvelimet'


class SMTPPassword(models.Model):
    smtp_server = models.ForeignKey(SMTPServer,
        related_name='smtp_passwords',
        verbose_name=u'SMTP-palvelin',
    )

    person = models.ForeignKey(Person,
        related_name='smtp_passwords',
        verbose_name=u'Henkilö',
    )

    password_hash = models.CharField(
        max_length=255,
        verbose_name=u'Salasanan tarkiste',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'Luotu'
    )

    @classmethod
    def create_for_domain_and_person(cls, domain, person, hash_module=md5_crypt):
        smtp_server = domain.smtp_servers.first()
        pw = generate_machine_password()

        with transaction.atomic():
            cls.objects.filter(smtp_server=smtp_server, person=person).delete()
            obj = cls(smtp_server=smtp_server, person=person, password_hash=hash_module.encrypt(pw))
            obj.save()

        return pw, obj

    class Meta:
        verbose_name = u'SMTP-salasana'
        verbose_name_plural = u'SMTP-salasanat'
