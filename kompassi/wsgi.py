import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kompassi.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling


application = Cling(MediaCling(get_wsgi_application()))
