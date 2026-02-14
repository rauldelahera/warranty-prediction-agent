"""
Centralized configuration for Warranty Prediction Agent.
Portfolio project - uses free Gemini API.
"""
import os

# Detect environment: "local" or "cloud"
ENVIRONMENT = "cloud" if os.getenv("K_SERVICE") or os.getenv("CLOUD_RUN_SERVICE") else "local"

# Proxy settings (optional - only if you're behind a corporate firewall)
# Leave empty for most users
http_proxy = os.getenv("HTTP_PROXY")
https_proxy = os.getenv("HTTPS_PROXY")
PROXIES = {
    "http": http_proxy,
    "https": https_proxy,
} if http_proxy or https_proxy else None

# Gemini API Configuration (FREE tier available)
# Get your free API key at: https://aistudio.google.com/app/apikey
GEMINI_API = {
    "model": "gemini-1.5-flash",  # Free tier: 15 req/min, 1M tokens/day
    "api_key": os.getenv("GEMINI_API_KEY"),  # Set this in your environment
}

# BigQuery Configuration
# TODO: Create your own GCP project or use BigQuery sandbox (free)
# Free BigQuery sandbox: https://cloud.google.com/bigquery/docs/sandbox
BIGQUERY = {
    "project": os.getenv("GCP_PROJECT_ID", "warranty-prediction-demo"),
}

# Debug mode enabled when running locally
DEBUG = ENVIRONMENT == "local"

# Print config on startup (debug only)
if DEBUG:
    print(f"🔧 Environment: {ENVIRONMENT}")
    print(f"🤖 Model: {GEMINI_API['model']}")
    print(f"📊 BigQuery Project: {BIGQUERY['project']}")
    print(f"🌐 Proxy: {PROXIES if PROXIES else 'None'}")
    print(f"🔍 Debug: ON")
