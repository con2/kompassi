def core_context(request):
    from django.conf import settings
    from .views import core_profile_menu_items

    return dict(
        settings=settings,
        core_profile_menu_items=core_profile_menu_items(request),
        ANALYTICS_ACCOUNT=getattr(settings, 'ANALYTICS_ACCOUNT', None),
        DEFAULT_FROM_EMAIL=getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@example.com')
    )
