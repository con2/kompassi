import logging

from oauth2_provider.oauth2_validators import OAuth2Validator


logger = logging.getLogger("kompassi")


class CustomOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = None

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
