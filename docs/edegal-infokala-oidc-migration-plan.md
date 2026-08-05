# Migrate Edegal and Infokala-tracon to Kompassi OIDC

Companion to `docs/oauth-oidc-consumer-inventory.md` (read that first for full
ecosystem context). This is the execution plan for the two apps we're
actively taking through the OIDC migration.

## Scope decisions (already made, recap only)

- **Tracontent-premium**: being sunset (static copy of current sites). Not migrated.
- **Infotv-tracon**: no migration planned. Sole using event (Tracon) owns this, not us.
- **Konsti** and **Kirppu** (kirppu.tracon.fi specifically): each has its own "2nd
  party" team already doing an OIDC migration independently. Not our work.
  `kirppu.desucon.fi` (a separate deployment of the same Kirppu codebase,
  authenticated via a JWT handshake with desucon.fi, not Kompassi at all —
  see the inventory doc) stays out of scope regardless.
- **Edegal** and **Infokala-tracon**: the two remaining apps on legacy Kompassi
  OAuth2 that are ours to actively migrate. This document covers both.

Both currently vendor the _same_ hand-rolled `kompassi_oauth2` Django app
(bare `requests_oauthlib.OAuth2Session`, no OIDC support, keyed off
Kompassi's legacy `/api/v2/people/me` REST endpoint). Neither app uses
`requests_oauthlib`/`oauthlib` for anything else, so the dependency can be
dropped entirely once migrated.

## Chosen approach: `mozilla-django-oidc`

Replace the vendored `kompassi_oauth2` app in both with
[`mozilla-django-oidc`](https://mozilla-django-oidc.readthedocs.io/) (actively
maintained — v5.0.1, Dec 2025) rather than hand-rolling another OIDC client.
This is the actual "standardize" step — both apps end up depending on the
same well-known public library instead of a bespoke one, which is much lower
maintenance burden and is what makes a future non-Kompassi IdP swap tractable.

The two migrations are the same shape with different `verify_claims`/
`update_user` logic. Do edegal first (simpler), then copy-adapt for infokala.

## Kompassi-side prerequisites (do once, before touching either app)

Register new OIDC Applications in Kompassi's Django admin
(`/admin/oauth2_provider/application/`), one per site, **`algorithm=RS256`**
(required for id_token signing — confirmed live against `kompassi.eu`'s
discovery document, which advertises `RS256` and `HS256`):

| App                          | Hostname           | New redirect URI                              |
| ---------------------------- | ------------------ | --------------------------------------------- |
| Edegal (production)          | conikuvat.fi       | `https://conikuvat.fi/admin/oidc/callback/`   |
| Edegal (larppikuvat)         | larppikuvat.fi     | `https://larppikuvat.fi/admin/oidc/callback/` |
| Infokala-tracon (production) | infokala.tracon.fi | `https://infokala.tracon.fi/oidc/callback/`   |

(Add staging/dev variants the same way, against `dev.kompassi.eu`, if you want
to test before touching production Kompassi Applications.)

Note the redirect path differs per app because edegal currently mounts its
auth routes under `/admin/` (`edegal_site/urls.py`: `path("admin/",
include("kompassi_oauth2.urls"))`, "must be after kompassi_oauth2 as we mount
it under /admin to pass proxy") while infokala mounts at the root
(`infokala_tracon/urls.py`: `path("", include("kompassi_oauth2.urls"))`).
Keep the same mount points for the new `mozilla_django_oidc.urls` include so
nothing else about the URL structure changes.

**Known Kompassi OIDC endpoints** (production; for staging swap `kompassi.eu`
→ `dev.kompassi.eu`), confirmed live via
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
family_name=request.user.person.surname,
given_name=request.user.person.first_name,
groups=[group.name for group in request.user.groups.all()],
name=request.user.person.full_name,
```

Plus the toolkit default `sub` = `str(request.user.pk)` (a stable numeric
Django User pk). **There is no `username`/`preferred_username` claim.** This
matters for account-continuity design below.

## Account continuity (read before writing the backend)

Both apps' current `kompassi_oauth2` backend links accounts by Kompassi's
legacy `username` string (`User.objects.get_or_create(username=kompassi_user['username'])`).
OIDC exposes no equivalent claim, so **do not try to match on username**.

Instead, rely on `mozilla-django-oidc`'s **default** `filter_users_by_claims`,
which matches by `email__iexact`. Both apps already store `email` on every
Django `User` from the legacy flow (`user_attrs_from_kompassi`'s `email`
mapping), so existing editor/admin accounts will reattach automatically on
their first OIDC login, with zero data migration needed. Do not override
`filter_users_by_claims`.

Caveat to flag, not block on: if a specific editor's Kompassi email changed
since they last logged in, they'll get a fresh account instead of reattaching
to their old one. Both apps have small editor counts — acceptable to fix by
hand (reassign permissions/merge) if it ever actually happens; not worth
building tooling for.

## Common migration recipe

Verified against `mozilla-django-oidc`'s actual source
(`mozilla_django_oidc/auth.py`, `OIDCAuthenticationBackend`) — method names
and default behavior below are accurate as of v5.0.1, not guessed.

1. **Dependency**: add `mozilla-django-oidc` (`pip`/`uv add`), drop
   `requests-oauthlib`/`oauthlib` once the old app is removed (confirmed
   unused elsewhere in both repos).

2. **`settings.py`**:

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
   `KOMPASSI_API_V2_USER_INFO_URL`/`KOMPASSI_OAUTH2_SCOPE` settings.

3. **`urls.py`**: replace `include("kompassi_oauth2.urls")` with
   `include("mozilla_django_oidc.urls")` at the _same mount point_ each app
   already uses (see redirect URI table above). The login-initiating view is
   named `oidc_authentication_init` — point `LOGIN_URL` at it (with the same
   `admin/` or root prefix as today).

4. **New backend module** (e.g. `kompassi_oidc/backends.py`, replacing the
   `kompassi_oauth2` package), subclassing
   `mozilla_django_oidc.auth.OIDCAuthenticationBackend`:
   - `verify_claims(self, claims)` — return `True`/`False` to allow/reject
     login. This is the per-app gate; see below. (Default implementation just
     checks `"email" in claims` — always override this.)
   - `filter_users_by_claims` — **do not override**, keep the email-matching
     default (see "Account continuity" above).
   - `update_user(self, user, claims)` — currently a no-op in the base class.
     Override to set `first_name`/`last_name` from `given_name`/
     `family_name`, derive `is_staff`/`is_superuser` from `claims["groups"]`,
     sync groups into Django's `Group` model (per-app, see below), `save()`,
     return `user`.
   - `create_user` — leave as default (derives a username from email); no
     legacy username to preserve for brand-new accounts.

5. Once verified in production, delete the old `kompassi_oauth2` package and
   its `INSTALLED_APPS`/`AUTHENTICATION_BACKENDS` entries. Consider keeping
   the _old_ Kompassi Application (client id/secret) registered-but-unused
   for one release as a fast rollback path (see "Rollback" below).

## Edegal-specific

Files: `backend/kompassi_oauth2/` (delete after cutover) → new
`backend/kompassi_oidc/`. `backend/edegal_site/settings.py`,
`backend/edegal_site/urls.py`. Feature flag `EDEGAL_USE_KOMPASSI_OAUTH2`
gates whether the auth routes mount at all today — carry this flag forward
(rename if you like, e.g. `EDEGAL_USE_KOMPASSI_OIDC`) rather than removing
the toggle.

Two sites, two `KOMPASSI_EDITOR_GROUP` values (env `KOMPASSI_EDITOR_GROUP`,
default `"conikuvat-staff"`; `larppikuvat.vars.yaml` overrides to
`"larppikuvat-staff"`). `KOMPASSI_ADMIN_GROUP` (default `"admins"`) shared.

```python
def verify_claims(self, claims):
    return settings.KOMPASSI_EDITOR_GROUP in claims.get("groups", [])

def update_user(self, user, claims):
    groups = claims.get("groups", [])
    user.first_name = claims.get("given_name", "")
    user.last_name = claims.get("family_name", "")
    user.is_superuser = settings.KOMPASSI_ADMIN_GROUP in groups
    user.is_staff = settings.KOMPASSI_EDITOR_GROUP in groups
    # only sync groups relevant to this app, matching current filtered behavior
    relevant = {settings.KOMPASSI_ADMIN_GROUP, settings.KOMPASSI_EDITOR_GROUP}
    user.groups.set([
        Group.objects.get_or_create(name=name)[0]
        for name in groups if name in relevant
    ])
    user.save()
    return user
```

This preserves current behavior exactly: non-editors are rejected at login
(`verify_claims` returning `False` surfaces as an authentication failure —
match today's `LOGIN_FAILED` Finnish error message UX if you want parity,
it's currently rendered by `CallbackView` in the old code).

**Aside on edegal's separate rewrite plan**: `spec/rewrite.md` already
targets a full Next.js + Auth.js + Kompassi OIDC rewrite, not started (no
auth code exists in `frontend-next/` yet). This Django-side swap is smaller,
faster, and decoupled from that rewrite's timeline — do it regardless of
whether/when the rewrite happens. If the rewrite does eventually land, this
work (a few hundred lines) is a fully acceptable sunk cost for de-risking the
legacy auth flow now rather than waiting indefinitely.

## Infokala-tracon-specific

Files: `kompassi_oauth2/` (delete after cutover) → new `kompassi_oidc/`.
`infokala_tracon/settings.py`, `infokala_tracon/urls.py` (mounted at root:
`path("", include(...))`).

Unlike edegal, infokala's current `CallbackView` does **not** gate login on
group membership at all — it only checks `user.is_active` (Django default
`True`). Authorization is entirely deferred to per-event checks in
`infokala_tracon/views.py`'s `is_user_allowed_to_access(user, event)`, which
tests `user.is_superuser` or membership in a set of per-event **templated**
group names (`INFOKALA_ACCESS_GROUP_TEMPLATES` in `settings.py`, e.g.
`"{kompassi_installation_slug}-{event_slug}-labour-jv"`). This logic reads
`user.groups` (Django's own, persisted) and needs **no changes at all** — it
doesn't care how those groups got there.

What it does need: the _entire_ flat `groups` claim list mirrored into
Django's `Group` model on every login (current backend does this
unfiltered — no allowlist, unlike edegal), so that whatever event-specific
group names show up are already `Group.objects.get_or_create`'d and
attached to the user before the view-level check runs.

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

## Verification plan

Test against `dev.kompassi.eu` with freshly registered dev OIDC Applications
before touching production Kompassi Applications or either app's production
deployment. Per app:

1. An existing editor/admin account logs in via OIDC for the first time →
   confirm it reattaches to the **same** existing Django `User` (check by id,
   not just "a session was created") rather than creating a duplicate.
2. A non-member Kompassi account: edegal should reject it outright
   (`verify_claims` → `False`); infokala should let it log in with no
   elevated `is_staff`/`is_superuser` and no event access.
3. Change a test account's Kompassi group membership, log in again, confirm
   `is_staff`/`is_superuser` (and, for infokala, per-event access) updates on
   the next login — both gaining and losing access.
4. Infokala only: exercise `is_user_allowed_to_access` end-to-end for at
   least one real templated group pattern against a real (or realistic test)
   event slug.
5. Roll out to staging deployments first, then production, one app at a
   time — edegal first.

## Rollback

Keep the old `kompassi_oauth2` app and its legacy Kompassi Application
(client id/secret) intact and registered until the new flow has been
verified in production for a while. Reverting is a `settings.py`/`urls.py`
change back to the old include/backend — no data was touched (both flows
resolve to the same `User` rows via `email`), so it's safe to flip back and
forth if something looks wrong.
