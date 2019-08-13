import os


def config_string_to_bool(setting):
    if setting.lower() in ("true", "yes", "on"):
        return True
    else:
        return False


# Core App Settings
APP_NAME = os.environ.get("APP_NAME", "DEV")

# Database Settings
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://127.0.0.1:27017/dos_monitor")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Scheduling Settings
CHECK_RATE_MINUTES = int(os.environ.get("CHECK_RATE_MINUTES", "5"))
STATUS_UPDATE_RATE_MINUTES = int(os.environ.get("STATUS_UPDATE_RATE_MINUTES", "60"))

# UEC DoS Settings
UEC_DOS_USERNAME = os.environ.get("UEC_DOS_USERNAME")
UEC_DOS_PASSWORD = os.environ.get("UEC_DOS_PASSWORD")
UEC_DOS_BASE_URL = os.environ.get("UEC_DOS_BASE_URL")

UEC_DOS_USERNAME_DIGITAL = os.environ.get("UEC_DOS_USERNAME_DIGITAL")
UEC_DOS_PASSWORD_DIGITAL = os.environ.get("UEC_DOS_PASSWORD_DIGITAL")

# Slack Notification Settings
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "#random")
SLACK_ENABLED = config_string_to_bool(os.environ.get("SLACK_ENABLED", ""))

# SMS Notification Settings
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")
MOBILE_NUMBER = os.environ.get("MOBILE_NUMBER")
SMS_ENABLED = config_string_to_bool(os.environ.get("SMS_ENABLED", ""))

ROLLBAR_ACCESS_TOKEN = os.environ.get("ROLLBAR_ACCESS_TOKEN", "")

# Basic Auth Settings
BASIC_AUTH_USERNAME = os.environ.get("BASIC_AUTH_USERNAME", "user")
BASIC_AUTH_PASSWORD = os.environ.get("BASIC_AUTH_PASSWORD", "pass")
BASIC_AUTH_FORCE = config_string_to_bool(os.environ.get("BASIC_AUTH_FORCE", "True"))

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")
