import json
from datetime import datetime, date
from functools import wraps

from jsonschema import ValidationError as JSONValidationError

from django.conf import settings
from django.forms import ValidationError as DjangoValidationError
from django.http import JsonResponse, HttpResponse, Http404


# https://djangosnippets.org/snippets/1304/
def http_basic_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        from django.contrib.auth import authenticate, login
        if request.META.has_key('HTTP_AUTHORIZATION'):
            authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                auth = auth.strip().decode('base64')
                username, password = auth.split(':', 1)
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
        return func(request, *args, **kwargs)
    return _decorator


class NotAuthorized(RuntimeError):
    pass


def api_view(view_func):
    @wraps(view_func)
    def _decorator(request, *args, **kwargs):
        try:
            result = view_func(request, *args, **kwargs)
        except NotAuthorized as e:
            return JsonResponse(
                dict(error='Unauthorized'),
                status=401,
                safe=False,
            )
        except Http404 as e:
            return JsonResponse(
                dict(error='Not Found'),
                status=404,
                safe=False,
            )
        except (JSONValidationError, DjangoValidationError) as e:
            return JsonResponse(
                dict(error='Bad Request'),
                status=400,
                safe=False,
            )

        return JsonResponse(result, safe=False)

    return _decorator


def api_login_required(view_func):
    @wraps(view_func)
    @http_basic_auth
    def _decorator(request, *args, **kwargs):
        if (not request.user.is_anonymous()) and (
            request.user.is_superuser or
            request.user.groups.filter(name=settings.KOMPASSI_APPLICATION_USER_GROUP).exists()
        ):
            return view_func(request, *args, **kwargs)
        else:
            raise NotAuthorized()

    return _decorator
