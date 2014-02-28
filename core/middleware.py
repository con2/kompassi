class PageWizardMiddleware(object):
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
        elif request.path in related:
            pass
        else:
            from core.utils import page_wizard_clear
            page_wizard_clear(request)

        return None