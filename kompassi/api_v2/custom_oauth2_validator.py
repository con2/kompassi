import logging

from oauth2_provider.oauth2_validators import OAuth2Validator

logger = logging.getLogger(__name__)


class CustomOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = None

    def get_userinfo_claims(self, request):
        claims = super().get_userinfo_claims(request)
        # Additional properties returned from /oidc/userinfo/
        if "phone" in request.scopes:
            claims["phone"] = request.user.person.normalized_phone_number
        return claims

    def get_additional_claims(self, request):
        return dict(
            email=request.user.person.email,
            email_verified=request.user.person.is_email_verified,
            family_name=request.user.person.surname,
            given_name=request.user.person.first_name,
            groups=[group.name for group in request.user.groups.all()],
            name=request.user.person.full_name,
        )
