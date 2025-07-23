from django.utils.translation import get_language_from_request


def get_other_language(current_language_code):
    if current_language_code == "fi":
        return "en", "In English…"
    else:
        return "fi", "Suomeksi…"


def core_context(request):
    from django.conf import settings

    from .views import core_profile_menu_items

    current_language_code = get_language_from_request(request)
    other_language_code, other_language_name = get_other_language(current_language_code)

    return dict(
        current_language_code=current_language_code,
        settings=settings,
        core_profile_menu_items=core_profile_menu_items(request),
        other_language_code=other_language_code,
        other_language_name=other_language_name,
        # google analytics deactivated on admin pages for privacy
        is_admin_page="/admin" in request.path,
    )
