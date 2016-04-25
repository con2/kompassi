# Kompassi SSO for Confluence

**WARNING**: This information is out of date. Current approach is to sync users directly to Crowd internal directory. SSO token management is implemented in [kompassi-atlasso](https://github.com/tracon/kompassi-atlasso).

Kompassi integrates with Atlassian Crowd to provide single sign-on (SSO) using Kompassi accounts for Confluence, Jira and other Crowd-enabled applications. The main use case in Tracon is to provide seamless transitioning from Kompassi to our wiki that houses instructions for volunteer workers.

Due to Crowd being a somewhat heavy closed-source application, we do not use Crowd as an authentication or authorization backend for Kompassi at Tracon. There are Django authentication backend implementations for the Crowd REST API but we do not use one. Instead, we first authenticate the user against the authentication backend configured in Django, which in our case is `django-auth-ldap` to our [FreeIPA](FREEIPA.md). Only after this authentication succeeds will we then fetch an SSO token from the Crowd REST API. This allows us to stay somewhat independent of Crowd as Crowd is only used to provide SSO to Atlassian applications.

Please refer to the sequence diagram below for further information. TL;NOTE "keksi" is Finnish for "cookie". Errata to the diagram: Instead of `/login?next=...`, we set the Confluence `login.url` to `https://kompassi.tracon.fi/crowd?next=...` which reuses an existing Kompassi session if present or redirects to the login page otherwise. The view is implemented in `atlassian_integration/views.py`.

![A non-logged-in user wishes to access a document in Confluence](https://raw.githubusercontent.com/japsu/kompassi/master/docs/crowd_sso_sequence.png)

## Atlassian documentation references

* https://developer.atlassian.com/display/CROWDDEV/JSON+Requests+and+Responses
* https://developer.atlassian.com/display/CROWDDEV/Crowd+REST+Resources#CrowdRESTResources-CrowdSSOTokenResource

## Enforce SSO for Jira dashboard

Jira has an ugly default dashboard that is shown to anonymous users. It includes an evil login form that can be disabled by configuration, but the dashboard remains available to anonymous users.

To stop this form from being shown to anonymous users, redirect all anonymous users to Kompassi SSO by `nginx` configuration:

    location / {
        proxy_pass http://127.0.0.1:9012;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        if ($http_cookie !~ 'crowd.token_key') {
            rewrite ^(.*)$ https://kompassi.tracon.fi/crowd?next=https://jira.tracon.fi$1 last;
        }
    }

## Validation factors

When authenticating to Crowd, one needs to provide so-called validation factors that are then used to determine if the session is still valid from Crowd's point of view. These need to match exactly or the session is torn down. It was somewhat labourious to find out which validation factors are being used.

In our setup (Confluence with bundled Tomcat behind an nginx proxy) they are as follows:
* `remote_address`: always `127.0.0.1` (note that it is spelled `remote_address`, not `remote_addr` as in `request.META['REMOTE_ADDR']`)
* `X-Forwarded-For`: as set by nginx in the request headers when configured by `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` (basically the real IP address of the client).
