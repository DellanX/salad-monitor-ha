from datetime import timedelta

MANUFACTURER = "Salad GPU Service"
MODEL = "Salad GPU Monitor"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)
DOMAIN = "salad_monitor"
DEFAULT_PORT = 8000
HEALTH_ENDPOINTS = ("/api/v1/health", "/health")
