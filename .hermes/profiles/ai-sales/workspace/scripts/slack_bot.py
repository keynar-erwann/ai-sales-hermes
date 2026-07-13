import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configuration
TOKEN = "xoxb-YOUR-SLACK-BOT-TOKEN"  # Remplace par ton vrai token bot
CHANNEL = "C0123456789" # ID de ton canal Slack
PENDING = "/root/.hermes/profiles/ai-sales/workspace/review-queue/pending"
APPROVED = "/root/.hermes/profiles/ai-sales/workspace/review-queue/approved"

client = WebClient(token=TOKEN)

def listen_for_approvals():
    try:
        # Récupère les messages du canal
        result = client.conversations_history(channel=CHANNEL, limit=5)
        for msg in result['messages']:
            if "APPROVE" in msg['text']:
                filename = msg['text'].split("APPROVE")[1].strip()
                approve_and_send(filename)
    except SlackApiError as e:
        print(f"Error: {e}")

def approve_and_send(filename):
    src = os.path.join(PENDING, filename)
    dst = os.path.join(APPROVED, filename)
    if os.path.exists(src):
        os.rename(src, dst)
        # Appel du script d'envoi
        import subprocess
        subprocess.run(["python3", "/root/.hermes/profiles/ai-sales/workspace/scripts/smtp_sender.py", dst])
        print(f"Processed: {filename}")

if __name__ == "__main__":
    while True:
        listen_for_approvals()
        time.sleep(10)
