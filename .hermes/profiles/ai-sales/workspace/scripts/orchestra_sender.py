import smtplib
import os
import sys
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("/root/.hermes/profiles/ai-sales/workspace/.env")

def send_production_email(recipient_email, subject, content):
    # Fetching credentials from environment variables
    smtp_host = os.getenv("SMTP_HOST", "sandbox.smtp.mailtrap.io")
    smtp_port = int(os.getenv("SMTP_PORT", 2525))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not smtp_user or not smtp_password:
        return False, "SMTP credentials not found in environment."

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'ai-sales@orchestra.com'
    msg['To'] = recipient_email
    msg.set_content(content)
    
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 orchestra_sender.py <recipient> <subject> <content_file>")
        sys.exit(1)
        
    recipient = sys.argv[1]
    subject = sys.argv[2]
    with open(sys.argv[3], 'r') as f:
        content = f.read()
    
    success, result = send_production_email(recipient, subject, content)
    print(result)
