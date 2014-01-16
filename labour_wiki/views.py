from django.shortcuts import render


def labour_wiki_required(view_func):
    @wraps(view_func)
    @worker_required
    @labour_event_required
    def wrapper(request, event, labour_space):
        labour_space = get_object_or_404(LabourWikiSpace, event=event, space__slug=labour_space)
        return view_func(request, event, labour_space)
    return wrapper


@require_http_methods(['GET', 'POST'])
@labour_wiki_required
def labour_wiki_page_view(self, event, labour_space, page='index'):
    try:
        page = Page.objects.get(space=labour_space.space, page=page)
    except Page.DoesNotExist:
        page = Page(space=labour_space.space, page)

    form = initialize_form(Page, request, instance=page, prefix='page')

    if request.method == 'POST':
        if form.is_valid():
            todo_save()
            return redirect('labour_wiki_page_view', event.slug, labour_space.slug, page.path)

    vars = dict(
        event=event,
        labour_space=labour_space,
        page=page,
    )

    return render(request, 'labour_wiki_page_view.jade', vars)
