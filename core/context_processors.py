def core_context(request):
    from django.conf import settings
    from .views import core_profile_menu_items

    vars = dict(
        settings=settings,
        core_profile_menu_items=core_profile_menu_items(request),
    )

    for key in [
        'ANALYTICS_ACCOUNT',
        'APPLICATION_NAME',
        'DEFAULT_FROM_EMAIL',
        'TURSKA_ACCOUNT_BRANDING',
        'TURSKA_ACCOUNT_BRANDING_2ND_PERSON_ADESSIVE',
        'TURSKA_ACCOUNT_BRANDING_ADESSIVE',
        'TURSKA_INSTALLATION_NAME',
        'TURSKA_INSTALLATION_NAME_GENITIVE',
        'TURSKA_INSTALLATION_NAME_ILLATIVE',
    ]:
        vars[key] = getattr(settings, key, key)

    return vars