from django.shortcuts import get_object_or_404, render

from core.models import Event

def labour_signup_view(request, event):
	print event
	event = get_object_or_404(Event, slug=event)

	vars = dict(
		event=event
	)

	return render(request, 'labour_signup.jade', vars)
