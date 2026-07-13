import os
import subprocess
import json

# Configuration
PENDING_QUEUE = "/root/.hermes/profiles/ai-sales/workspace/review-queue/pending"
WEBHOOK_URL = "https://hooks.slack.com/services/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"

def get_pending_drafts():
    return [f for f in os.listdir(PENDING_QUEUE) if f.endswith(".md")]

def send_to_slack(filename):
    filepath = os.path.join(PENDING_QUEUE, filename)
    with open(filepath, 'r') as f:
        content = f.read(500)
    
    payload = {
        "text": f"🚨 *Nouveau brouillon à valider : {filename}*\n\n{content}...\n\nPour valider, confirmez dans ce fil."
    }
    
    # Use curl to send to Slack directly
    subprocess.run([
        "curl", "-X", "POST", "-H", "Content-type: application/json",
        "--data", json.dumps(payload),
        WEBHOOK_URL
    ], capture_output=True)
    print(f"Sent {filename} to Slack")

def main():
    drafts = get_pending_drafts()
    if not drafts:
        print("No pending drafts.")
        return
    
    for draft in drafts:
        send_to_slack(draft)

if __name__ == "__main__":
    main()
