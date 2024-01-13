# Access management

The `access` module is responsible for various tasks related to managing user access to computing resources.

## Main features

### E-mail alias management for inbound e-mail

Given a `EmailAliasDomain` and an `EmailAliasType`, one can create `EmailAlias`es for `Person`s. These `EmailAlias`es enable e-mail delivery from an alias address such as `someorganizer@tracon.fi` to their private e-mail address they have configured in their profile.

`EmailAlias`es can be either created manually from the Django admin or be automatically created via `GroupEmailAliasGrant`. The automatic facility can be used in conjunction with eg. the volunteer worker management module to create e-mail aliases for all organizers of an event.

Note that for the automatic facility to work, whatever changes the group membership must be hooked to call `GroupEmailAliasGrant.ensure_aliases`. This is done by eg. `Signup.apply_state`.

The MTA responsible for inbound e-mail for the domain must be configured to periodically refresh its aliases from `/api/v1/domains/your.domain.test/aliases.txt`. This uses HTTP basic authentication using app users (see `api/README`).

### SMTP server user management for outbound e-mail (work in progress)

In order to facilitate secure outbound e-mail with SPF, DKIM, DMARC and other TLA/ETLA/XETLAs, one or more `SMTPServer`s can be connected to one or more `EmailAliasDomain`s.

If such an `SMTPServer` exists for an `EmailAliasDomain`, an user with an `EmailAlias` in that domain can use the `/profile/aliases` view to request a password for that SMTP server. That password and their Kompassi username can then be used to send outbound e-mail using that SMTP server.

We do not use the Kompassi account password for this purpose due to the following reasons:

1. The **first principle of Kompassi account security** is to never enter the Kompassi account password anywhere else than `https://kompassi.eu/login`.
2. The Kompassi account password is hashed using an algorithm not commonly supported by MTAs.
3. We do not trust common MTAs to portably support strong password hashes.

In order to discourage people from manually setting the same password for SMTP use, or using a weak password, a secure SMTP password is automatically generated.

Because the user requesting an SMTP password is likely to try it out right after requesting the password, periodical refresh is not enough, but rather we need to make the act of requesting a password cause a user database refresh at the MTA. For this, updates will be pushed out using SSH/SFTP.

### Slack invitation management

The `Privilege` model is a generic facility for granting specific privileges by request to people who belong to one of the groups that grant access. A `Privilege` that is granted to a user is represented as `GrantedPrivilege`.

The only practical use so far has been self-service invitations to Slack for event volunteers. This is done using `Privilege`s that have their `grant_code` set to `access.privileges:invite_to_slack`. A `GroupPrivilege` connects a group of users to a `Privilege`, enabling them to request the said privilege using the `/profile/privileges` view.

The Slack invite process is as follows:

1. The volunteer signs up to the event and their application is accepted.
2. The volunteer receives a welcome message, usually via `mailings.Message`, informing them of the Slack community and giving a link to `/profile/privileges`.
3. The volunteer navigates there, finds they are eligible for access to a Slack community, accepts a disclaimer about giving their e-mail address to Slack and presses a button to request access.
4. Kompassi makes an API call to Slack, causing Slack to send an invitation to the provided e-mail address.
5. The volunteer receives an invitation e-mail from Slack and, following instructions contained therein, proceeds to register with Slack, gaining access to the Slack community.

Currently the integration is one way, ie. people can be invited to Slack but we do not manage their user accounts via Kompassi further. That is to say, disabling access from people who no longer need it must be done via the Slack administrative interface.
