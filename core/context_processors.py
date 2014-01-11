def core_context(request):
    from django.conf import settings
    return dict(
        settings=settings,
        ANALYTICS_ACCOUNT=getattr(settings, 'ANALYTICS_ACCOUNT', None),
        DEFAULT_FROM_EMAIL=getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@example.com')
    )