from django.core.urlresolvers import reverse
from django.template.loader import render_to_string


def url(view_name, *args):
    return reverse(view_name, args=args)


def render_string(request, template_name, vars):
    return render_to_string(template_name, vars, context_instance=RequestContext(request))


def login_redirect(request, view='core_login_view'):
    path = reverse(view)
    query = urlencode(dict(next=request.path))
    return HttpResponseRedirect("{path}?{query}".format(**locals()))


def get_next(request, default='/'):
    if request.method == 'GET':
        next = request.GET.get('next', None)
    elif request.method == 'POST':
        next = request.POST.get('next', None)
    else:
        raise NotImplemented(request.method)

    return next if next else default


def next_redirect(request, default='/'):
    next = get_next(request, default)
    return redirect(next)
