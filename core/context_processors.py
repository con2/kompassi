# encoding: utf-8



from django.utils.translation import get_language_from_request


def get_other_language(current_language_code):
    if current_language_code == 'fi':
        return 'en', 'In English…'
    else:
        return 'fi', 'Suomeksi…'


def core_context(request):
    from django.conf import settings
    from .views import core_profile_menu_items

    current_language_code = get_language_from_request(request)
    other_language_code, other_language_name = get_other_language(current_language_code)

    vars = dict(
        current_language_code=current_language_code,
        settings=settings,
        core_profile_menu_items=core_profile_menu_items(request),
        other_language_code=other_language_code,
        other_language_name=other_language_name,
        show_language_warning=(other_language_code == 'fi'),
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