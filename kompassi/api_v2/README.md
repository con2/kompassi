# Kompassi API v2

This module provides, most importantly the `/api/v2/people/me` endpoint used by OAuth2 clients performing user authentication and authorization against Kompassi.

## API version numbering

Currently the version numbering is mostly based on the authentication method:

- `v1`: HTTP basic authentication using application users
- `v2`: OAuth2 authentication

Public resources are under `v1`. The `v2` API is mostly final. The `v1` API is growing organically and will be deprecated at some point. When a proper CRUD REST API for most resources is designed, it will become `v3`.

## Legacy OAuth2

An OAuth2 provider is implemented using the `oauthlib` and `django-oauth-toolkit` libraries. Its views are mounted in the `urls.py` of this app.

A user info endpoint is provided at `/api/v2/people/me` for purposes of OAuth2 based single sign-on. First perform the OAuth2 authentication dance to get a token, and then use that token to get current user information from that endpoint.

At the time of implementation the OpenID Connect specification was not yet ready, but some apps rely on this behaviour, so another OIDC provider is implemented at `/oidc/`.

## OpenID Connect

Using the same `oauthlib` and `django-oauth-toolkit`, there is a standard OpenID Connect provider mounted at `/oidc/`. Query for its configuration information at `/oidc/.well-known/openid-configuration/`. Note that this deviates from Kompassi conventions in that the trailing slash is required, not optional as in most Kompassi endpoints.

To enable local development with clients that require the `RS256` algorithm to validate the JWT tokens issued by Kompassi, you need to create an RSA private key and pass it to Kompassi via environment variables:

    openssl genrsa -out local.key 4096
    export OIDC_RSA_PRIVATE_KEY="$(<local.key)"
    docker compose up

## This app was a mistake and should be integrated into `core`

One of two approaches could be taken to the placement of API views within Kompassi:

1. put them all in the `api` app
2. put them in the module where the models they operate on are

This app was created with the first approach in mind. However, if Kompassi was to have a decent CRUD REST API for all resource types, it would make `api` a God App with dependencies to just about everything.

Hence this app was a mistake and its current functionality should be integrated into `core`, with further views placed in whatever app the models are in.
