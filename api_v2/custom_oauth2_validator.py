import logging

from oauth2_provider.oauth2_validators import OAuth2Validator


logger = logging.getLogger("kompassi")


class CustomOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = None

    def validate_code(self, client_id, code, client, request, *args, **kwargs):
        """
        Stop users with no verified email address from logging in to external apps.
        TODO this approach does not give them a proper error message
        """
        if not request.user.person.is_email_verified:
            logger.warning(
                "User %s tried to log in via OIDC with unverified email address",
                request.user.id,
            )
            return False

        return super().validate_code(client_id, code, client, request, *args, **kwargs)

    def get_userinfo_claims(self, request):
        """
        Used by /oidc/userinfo/
        """
        claims = super().get_userinfo_claims(request)
        claims.update(
            email=request.user.person.email,
            display_name=request.user.person.display_name,
            groups=[group.name for group in request.user.groups.all()],
        )
        return claims
