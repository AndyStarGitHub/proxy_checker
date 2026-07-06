import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    TEST_URL: str = "https://api.ipify.org?format=json"
    TIMEOUT_SECONDS: int = 5
    FAST_THRESHOLD_MS: int = 1000  # any latency <= 1000ms is considered fast
    TEMPLATES_DIR: str = "templates"
    PROXY_BASE_DOMAIN: str = os.getenv("PROXY_BASE_DOMAIN", "http://default_user:default_pass@")


settings = Settings()
