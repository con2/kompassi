import logging

from oauth2_provider.oauth2_validators import OAuth2Validator

logger = logging.getLogger(__name__)


class CustomOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = None

    def get_additional_claims(self, request):
        return dict(
            email=request.user.person.email,
            family_name=request.user.person.surname,
            given_name=request.user.person.first_name,
            groups=[group.name for group in request.user.groups.all()],
            name=request.user.person.full_name,
        )
