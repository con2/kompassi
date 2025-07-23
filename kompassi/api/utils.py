import base64
import json
import logging
from functools import wraps

from django.conf import settings
from django.forms import ValidationError as DjangoValidationError
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jsonschema import (
    ValidationError as JSONValidationError,
)
from jsonschema import (
    validate,
)

from kompassi.access.cbac import default_cbac_required

logger = logging.getLogger(__name__)


# https://djangosnippets.org/snippets/1304/
def http_basic_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        from django.contrib.auth import authenticate, login

        if "authorization" in request.headers:
            authmeth, auth = request.headers["authorization"].split(" ", 1)
            if authmeth.lower() == "basic":
                auth = base64.decodebytes(auth.encode("UTF-8")).decode("UTF-8")  # fmh
                username, password = auth.split(":", 1)
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
        return func(request, *args, **kwargs)

    return _decorator


class NotAuthorized(RuntimeError):
    pass


class MethodNotAllowed(RuntimeError):
    pass


class BadRequest(RuntimeError):
    pass


def handle_api_errors(view_func):
    @wraps(view_func)
    def _decorator(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except (ValueError, JSONValidationError, DjangoValidationError, BadRequest):
            logger.exception("Bad Request at %s", request.path)
            return JsonResponse(
                dict(error="Bad Request"),
                status=400,
            )
        except NotAuthorized:
            logger.exception("Unauthorized at %s", request.path)
            response = JsonResponse(
                dict(error="Unauthorized"),
                status=401,
            )
            response["WWW-Authenticate"] = "Basic realm=api"
            return response
        except Http404:
            logger.exception("Not Found at %s", request.path)
            return JsonResponse(
                dict(error="Not Found"),
                status=404,
            )
        except MethodNotAllowed:
            logger.exception("Method Not Allowed at %s", request.path)
            return JsonResponse(
                dict(error="Not Found"),
                status=405,
            )

    return _decorator


def api_view(view_func):
    @wraps(view_func)
    @csrf_exempt
    @handle_api_errors
    def _decorator(request, *args, **kwargs):
        result = view_func(request, *args, **kwargs)

        if result is None:
            return HttpResponse("", status=204)
        elif isinstance(result, HttpResponse):
            return result
        else:
            return JsonResponse(result, safe=False)

    return _decorator


def api_login_required(view_func):
    @wraps(view_func)
    @http_basic_auth
    def _decorator(request, *args, **kwargs):
        if (not request.user.is_anonymous) and (
            request.user.is_superuser
            or request.user.groups.filter(name=settings.KOMPASSI_APPLICATION_USER_GROUP).exists()
        ):
            return view_func(request, *args, **kwargs)
        else:
            raise NotAuthorized()

    return _decorator


def cbac_api_view(view_func):
    """
    An API view that uses CBAC for authentication.

    Authentication can use either:
    1. HTTP Basic authentication for users in app group, or
    2. session authentication for superusers only.
    """
    return api_view(api_login_required(default_cbac_required(view_func)))


class JSONSchemaObject:
    """
    A mixin to use in conjunction with collections.namedtuple. For examples, see
    desuprofile_integration/models.py.
    """

    @classmethod
    def from_dict(cls, d):
        validate(d, cls.schema)
        attrs = [d.get(key, None) for key in cls._fields]
        return cls(*attrs)

    @classmethod
    def from_json(cls, s):
        return cls.from_dict(json.loads(s))
