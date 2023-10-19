import logging

from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.exceptions import FatalClientError


logger = logging.getLogger("kompassi")


class CustomOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = None

    def get_additional_claims(self, request):
        return dict(
            email=request.user.person.email,
            family_name=request.user.person.surname,
            given_name=request.user.person.first_name,
            groups=[group.name for group in request.user.groups.all()],
            name=request.user.person.display_name,
        )

    def save_bearer_token(self, token, request, *args, **kwargs):
        # TODO Visible error to user would probably require overriding AuthorizationView.
        if not request.user.person.is_email_verified:
            raise FatalClientError(
                "You need to verify your e-mail address before you can use Kompassi to log in to other services."
            )

        return super().save_bearer_token(token, request, *args, **kwargs)
