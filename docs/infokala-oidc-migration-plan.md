# Migrate Infokala-tracon to Kompassi OIDC

Companion to `docs/oauth-oidc-consumer-inventory.md` (read that first for full
ecosystem context). This is the execution plan for Infokala-tracon
(`con2/infokala-tracon`, infokala.tracon.fi), the last app on legacy Kompassi
OAuth2 that is ours to migrate.

## Scope decisions (already made, recap only)

- **Edegal**: done. Edegal v4 (Next.js, Auth.js v5) signs in with Kompassi OIDC
  and the Django app with the vendored `kompassi_oauth2` is gone.
- **Tracontent-premium**: being sunset (static copy of current sites). Not migrated.
- **Infotv-tracon**: no migration planned. Sole using event (Tracon) owns this, not us.
- **Konsti** and **Kirppu** (kirppu.tracon.fi specifically): each has its own "2nd
  party" team already doing an OIDC migration independently. Not our work.
  `kirppu.desucon.fi` (a separate deployment of the same Kirppu codebase,
  authenticated via a JWT handshake with desucon.fi, not Kompassi at all —
  see the inventory doc) stays out of scope regardless.

Infokala vendors a hand-rolled `kompassi_oauth2` Django app (bare
`requests_oauthlib.OAuth2Session`, no OIDC support, keyed off Kompassi's
legacy `/api/v2/people/me` REST endpoint). Nothing else in the repository
uses `requests_oauthlib`/`oauthlib`, so the dependency can be dropped once
migrated.

## Chosen approach: `mozilla-django-oidc`

Replace the vendored `kompassi_oauth2` app with
[`mozilla-django-oidc`](https://mozilla-django-oidc.readthedocs.io/) (actively
maintained — v5.0.1, Dec 2025) rather than hand-rolling another OIDC client.
Depending on a well-known public library instead of a bespoke one is much
lower maintenance burden and is what makes a future non-Kompassi IdP swap
tractable.

## Kompassi-side prerequisites

Register a new OIDC Application in Kompassi's Django admin
(`/admin/oauth2_provider/application/`), **`algorithm=RS256`** (required for
id_token signing; `kompassi.eu`'s discovery document advertises `RS256` and
`HS256`), with the redirect URI `https://infokala.tracon.fi/oidc/callback/`.
Register a dev variant against `dev.kompassi.eu` the same way to test before
touching the production Application.

Infokala mounts its auth routes at the root (`infokala_tracon/urls.py`:
`path("", include("kompassi_oauth2.urls"))`). Keep the same mount point for
the new `mozilla_django_oidc.urls` include so nothing else about the URL
structure changes.

**Kompassi OIDC endpoints** (production; for staging swap `kompassi.eu` →
`dev.kompassi.eu`), from
`curl https://kompassi.eu/oidc/.well-known/openid-configuration`:

```
authorization_endpoint: https://kompassi.eu/oidc/authorize/
token_endpoint:         https://kompassi.eu/oidc/token/
userinfo_endpoint:      https://kompassi.eu/oidc/userinfo/
jwks_uri:               https://kompassi.eu/oidc/.well-known/jwks.json
```

`mozilla-django-oidc` does not do discovery — these need to be set as literal
settings values (see below), not derived from a single discovery URL at
runtime.

**Claims exposed** (`kompassi/api_v2/custom_oauth2_validator.py`,
`get_additional_claims`), unconditionally in both the id_token and
`/oidc/userinfo/`, regardless of granted scope:

```python
email=request.user.person.email,
email_verified=request.user.person.is_email_verified,
family_name=request.user.person.surname,
given_name=request.user.person.first_name,
groups=[group.name for group in request.user.groups.all()],
name=request.user.person.full_name,
```

Plus the toolkit default `sub` = `str(request.user.pk)` (a stable numeric
Django User pk). **There is no `username`/`preferred_username` claim.** This
matters for account continuity below.

## Account continuity (read before writing the backend)

The current `kompassi_oauth2` backend links accounts by Kompassi's legacy
`username` string (`User.objects.get_or_create(username=kompassi_user['username'])`).
OIDC exposes no equivalent claim, so **do not try to match on username**.

Instead, rely on `mozilla-django-oidc`'s **default** `filter_users_by_claims`,
which matches by `email__iexact`. Every Django `User` from the legacy flow
already has `email` set (`user_attrs_from_kompassi`'s `email` mapping), so
existing accounts reattach automatically on their first OIDC login, with no
data migration. Do not override `filter_users_by_claims`.

Caveat to flag, not block on: if a user's Kompassi email changed since they
last logged in, they get a fresh account instead of reattaching to their old
one. Its groups and admin flags come back on that login anyway; anything else
tied to the old `User` row can be merged by hand if it ever actually happens.

## Migration recipe

Verified against `mozilla-django-oidc`'s source
(`mozilla_django_oidc/auth.py`, `OIDCAuthenticationBackend`) — method names
and default behavior below are accurate as of v5.0.1.

1. **Dependency**: add `mozilla-django-oidc` (`uv add`), drop
   `requests-oauthlib` from `pyproject.toml` and `kompassi_oauth2` from its
   `packages` list and the `Dockerfile` `COPY` once the old app is removed.

2. **`infokala_tracon/settings.py`**:

   ```python
   INSTALLED_APPS += ["mozilla_django_oidc"]

   AUTHENTICATION_BACKENDS = [
       "django.contrib.auth.backends.ModelBackend",
       "kompassi_oidc.backends.KompassiOIDCAuthenticationBackend",  # new
   ]

   OIDC_RP_CLIENT_ID = env("KOMPASSI_OAUTH2_CLIENT_ID")      # reuse existing env var names —
   OIDC_RP_CLIENT_SECRET = env("KOMPASSI_OAUTH2_CLIENT_SECRET")  # avoids extra K8s secret churn
   OIDC_OP_AUTHORIZATION_ENDPOINT = f"{KOMPASSI_HOST}/oidc/authorize/"
   OIDC_OP_TOKEN_ENDPOINT = f"{KOMPASSI_HOST}/oidc/token/"
   OIDC_OP_USER_ENDPOINT = f"{KOMPASSI_HOST}/oidc/userinfo/"
   OIDC_OP_JWKS_ENDPOINT = f"{KOMPASSI_HOST}/oidc/.well-known/jwks.json"
   OIDC_RP_SIGN_ALGO = "RS256"
   OIDC_RP_SCOPES = "openid email profile"
   ```

   Remove the old `KOMPASSI_OAUTH2_AUTHORIZATION_URL`/`_TOKEN_URL`/
   `KOMPASSI_API_V2_USER_INFO_URL`/`KOMPASSI_OAUTH2_SCOPE` settings. Keep
   `KOMPASSI_API_V2_EVENT_INFO_URL_TEMPLATE`: `infokala_tracon/event.py` looks
   up event names from the public `/api/v2/events/{slug}` endpoint without
   authentication, which is unrelated to login.

3. **`infokala_tracon/urls.py`**: replace `include("kompassi_oauth2.urls")`
   with `include("mozilla_django_oidc.urls")` at the root. The login-initiating
   view is named `oidc_authentication_init`; point `LOGIN_URL` (today
   `/oauth2/login`) at it.

4. **New backend module** `kompassi_oidc/backends.py`, replacing the
   `kompassi_oauth2` package, subclassing
   `mozilla_django_oidc.auth.OIDCAuthenticationBackend`:
   - `verify_claims(self, claims)` — return `True`/`False` to allow/reject
     login. The default just checks `"email" in claims`; override it (below).
   - `filter_users_by_claims` — **do not override**, keep the email-matching
     default (see "Account continuity" above).
   - `update_user(self, user, claims)` — a no-op in the base class. Override
     it (below).
   - `create_user` — leave as default (derives a username from email); no
     legacy username to preserve for brand-new accounts.

5. Once verified in production, delete the old `kompassi_oauth2` package and
   its `INSTALLED_APPS`/`AUTHENTICATION_BACKENDS` entries. Keep the _old_
   Kompassi Application (client id/secret) registered but unused for one
   release as a fast rollback path (see "Rollback" below).

## The backend

Infokala's current `CallbackView` does **not** gate login on group membership
— it only checks `user.is_active` (Django default `True`). Authorization is
entirely deferred to per-event checks in `infokala_tracon/views.py`'s
`is_user_allowed_to_access(user, event)`, which tests `user.is_superuser` or
membership in a set of per-event **templated** group names
(`INFOKALA_ACCESS_GROUP_TEMPLATES` in `settings.py`, e.g.
`"{kompassi_installation_slug}-{event_slug}-labour-jv"`). This logic reads
`user.groups` (Django's own, persisted) and needs **no changes** — it doesn't
care how those groups got there.

What it does need: the _entire_ flat `groups` claim list mirrored into
Django's `Group` model on every login (the current backend does this
unfiltered, with no allowlist), so that whatever event-specific group names
show up are already `Group.objects.get_or_create`'d and attached to the user
before the view-level check runs.

```python
def verify_claims(self, claims):
    return True  # no login-time gate today; keep parity, don't introduce one

def update_user(self, user, claims):
    groups = claims.get("groups", [])
    user.first_name = claims.get("given_name", "")
    user.last_name = claims.get("family_name", "")
    user.is_superuser = settings.KOMPASSI_ADMIN_GROUP in groups
    user.is_staff = settings.KOMPASSI_ADMIN_GROUP in groups
    user.groups.set([Group.objects.get_or_create(name=name)[0] for name in groups])
    user.save()
    return user
```

## Deployment

Infokala deploys with its own Helm chart (`chart/` in the infokala-tracon
repository). The Secret `infokala` keeps its `KOMPASSI_OAUTH2_CLIENT_ID` and
`KOMPASSI_OAUTH2_CLIENT_SECRET` keys; only their values change to the new
OIDC Application's credentials at cutover. For a rollback, put the old
values back.

## Verification plan

Test against `dev.kompassi.eu` with a freshly registered dev OIDC Application
before touching the production Application or deployment.

1. An existing account logs in via OIDC for the first time → confirm it
   reattaches to the **same** existing Django `User` (check by id, not just
   "a session was created") rather than creating a duplicate.
2. A Kompassi account in none of the relevant groups logs in with no
   elevated `is_staff`/`is_superuser` and no event access.
3. Change a test account's Kompassi group membership, log in again, confirm
   `is_staff`/`is_superuser` and per-event access update on the next login —
   both gaining and losing access.
4. Exercise `is_user_allowed_to_access` end-to-end for at least one real
   templated group pattern against a real (or realistic test) event slug.

## Rollback

Keep the old `kompassi_oauth2` app and its legacy Kompassi Application
(client id/secret) intact and registered until the new flow has been
verified in production for a while. Reverting is a `settings.py`/`urls.py`
change back to the old include/backend plus the old Secret values — no data
was touched (both flows resolve to the same `User` rows via `email`), so it's
safe to flip back and forth if something looks wrong.
