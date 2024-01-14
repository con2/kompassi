import logging

try:
    from .celery_app import app as celery_app
except ImportError:
    logger = logging.getLogger("kompassi")
    logger.warning("Failed to import Celery. Background tasks not available.", exc_info=True)
