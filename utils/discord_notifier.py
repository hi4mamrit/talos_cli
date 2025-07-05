import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_discord_message(message: str):
    """
    Sends a message to a Discord channel using a webhook URL.
    The message can be plain text or Markdown-formatted.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL not set in .env file")

    payload = {
        "content": f"📌 **Daily P0 Digest**\n\n{message}"
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code != 204:
        raise Exception(f"Discord webhook failed: {response.status_code}, {response.text}")
