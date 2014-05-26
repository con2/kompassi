def core_context(request):
    from django.conf import settings
    from .views import core_profile_menu_items

    vars = dict(
        settings=settings,
        core_profile_menu_items=core_profile_menu_items(request),
    )

    for key in [
        'ANALYTICS_ACCOUNT',
        'KOMPASSI_APPLICATION_NAME',
        'DEFAULT_FROM_EMAIL',
        'KOMPASSI_ACCOUNT_BRANDING',
        'KOMPASSI_ACCOUNT_BRANDING_2ND_PERSON_ADESSIVE',
        'KOMPASSI_ACCOUNT_BRANDING_ADESSIVE',
        'KOMPASSI_INSTALLATION_NAME',
        'KOMPASSI_INSTALLATION_NAME_GENITIVE',
        'KOMPASSI_INSTALLATION_NAME_ILLATIVE',
    ]:
        vars[key] = getattr(settings, key, key)

    return vars