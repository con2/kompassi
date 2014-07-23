import json
from datetime import datetime, date
from functools import wraps

from django.conf import settings
from django.http import HttpResponse


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


def json_default_handler(obj):
    if type(obj) in [date, datetime]:
        return obj.isoformat()
    else:
        return None


class NotAuthorized(RuntimeError):
    pass


def api_view(view_func):
    @wraps(view_func)
    def _decorator(request, *args, **kwargs):
        try:
            result = view_func(request, *args, **kwargs)
        except NotAuthorized as e:
            return HttpResponse(
                json.dumps(dict(error='Unauthorized')),
                status=401,
                mimetype='application/json'
            )

        return HttpResponse(json.dumps(result, default=json_default_handler), mimetype='application/json')

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


def pick_attrs(obj, *attr_names):
    return dict((attr_name, getattr(obj, attr_name)) for attr_name in attr_names)
