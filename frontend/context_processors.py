def frontend_context(request):
    from django.conf import settings
    return dict(
        ANALYTICS_ACCOUNT=getattr(settings, 'ANALYTICS_ACCOUNT', None),
        EVENT_URL=getattr(settings, 'EVENT_URL', 'http://localhost'),
        EVENT_NAME=getattr(settings, 'EVENT_NAME', 'Unnamed Event'),
        EVENT_NAME_GENITIVE=getattr(settings, 'EVENT_NAME_GENITIVE', "Unnamed Event's"),
        EVENT_NAME_ILLATIVE=getattr(settings, 'EVENT_NAME_ILLATIVE', "to Unnamed Event"),
        DEFAULT_FROM_EMAIL=getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@example.com')
    )