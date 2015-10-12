from django.core.urlresolvers import reverse
from django.template.loader import render_to_string


def url(view_name, *args):
    return reverse(view_name, args=args)


def render_string(request, template_name, vars):
    return render_to_string(template_name, vars, context_instance=RequestContext(request))

