from django.http import HttpResponse

METRICS_RESPONSE = """
# HELP kompassi_up Dummy metric to tell Prometheus we're up
# TYPE kompassi_up gauge
kompassi_up{} 1
""".lstrip()


def dummy_metrics_view(request):
    return HttpResponse(METRICS_RESPONSE, content_type="text/plain")
