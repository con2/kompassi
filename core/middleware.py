# encoding: utf-8

from django.utils.deprecation import MiddlewareMixin

from .page_wizard import page_wizard_clear


NEVER_BLOW_PAGE_WIZARD_PREFIXES = [
    # we have addresses like /desuprofile/confirm/475712413a0ddc3c7a57c6721652b75449bf3c89
    # that should not blow the page wizard when used within a signup page wizard flow
    '/desuprofile/confirm/',
]


class PageWizardMiddleware(MiddlewareMixin):
    """
    MIDDLEWARE_CLASSES = (
        # ...

        'core.middleware.PageWizardMiddleware'
    )

    Clear the page wizard when visiting a non-related page.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        related = request.session.get('core.utils.page_wizard.related', None)

        if related is None:
            pass
        elif request.method != 'GET':
            pass
        elif request.path in related:
            pass
        elif any(request.path.startswith(prefix) for prefix in NEVER_BLOW_PAGE_WIZARD_PREFIXES):
            pass
        else:
            page_wizard_clear(request)

        return None
