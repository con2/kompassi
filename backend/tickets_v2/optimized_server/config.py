import os

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

KOMPASSI_BASE_URL = os.getenv("KOMPASSI_BASE_URL", "https://kompassi.eu")
KOMPASSI_V2_BASE_URL = os.getenv("KOMPASSI_V2_BASE_URL", "https://v2.kompassi.eu")

# uvicorn/optimized_server
TICKETS_BASE_URL = os.getenv("TICKETS_BASE_URL", KOMPASSI_BASE_URL)
