# encoding: utf-8

from django.urls import reverse

from .utils import get_next, url


def page_wizard_init(request, pages):
    assert all(len(page) in [2, 3] for page in pages)

    steps = []
    all_related = set()

    for index, page in enumerate(pages):
        if len(page) == 2:
            name, title = page
            cur_related = []
        else:
            name, title, cur_related = page

        title = "{}. {}".format(index + 1, title)

        cur_related = set(cur_related)
        cur_related.add(name)
        cur_related = list(i if i.startswith('/') else url(i) for i in cur_related)
        all_related.update(cur_related)

        steps.append((name, title, cur_related))

    request.session['core.utils.page_wizard.steps'] = steps
    request.session['core.utils.page_wizard.related'] = list(all_related)


def page_wizard_clear(request):
    if 'core.utils.page_wizard.steps' in request.session:
        # raise RuntimeError('WHO DARES CALL PAGE_WIZARD_CLEAR')
        del request.session['core.utils.page_wizard.steps']
        del request.session['core.utils.page_wizard.related']


def page_wizard_vars(request):
    next = get_next(request)

    if 'core.utils.page_wizard.steps' in request.session:
        page_wizard = []
        active = False

        for name, title, related in request.session['core.utils.page_wizard.steps']:
            if active:
                next = name if name.startswith('/') else reverse(name)

            active = request.path in related
            page_wizard.append((title, active))

        return dict(
            page_wizard=page_wizard,
            next=next,
        )
    else:
        return dict(next=next)
