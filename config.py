from dataclasses import dataclass
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return value

def parse_recipients(recipients_str: str) -> List[str]:
    return [r.strip() for r in recipients_str.split(',') if r.strip()]

@dataclass
class TwilioConfig:
    account_sid: str = get_required_env("TWILIO_ACCOUNT_SID")
    auth_token: str = get_required_env("TWILIO_AUTH_TOKEN")
    messaging_service_sid: str = get_required_env("TWILIO_MESSAGING_SERVICE_SID")
    recipients: List[str] = None

    def __post_init__(self):
        self.recipients = parse_recipients(get_required_env("NOTIFICATION_RECIPIENTS"))

@dataclass
class AppConfig:
    base_url: str = "https://liverpoolfc.com"
    tickets_path: str = "/tickets/tickets-availability"
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
