# encoding: utf-8

from functools import wraps

from django.contrib.auth.decorators import login_required

from .models import Person
from .utils import login_redirect

def person_required(view_func):
    @login_required
    @wraps(view_func)
    def inner(request, *args, **kwargs):
        try:
            person = request.user.person
        except Person.DoesNotExist:
            return login_redirect(request, view='core_personify_view')

        return view_func(request, *args, **kwargs)

    return inner