import smtplib
import sys
from email.message import EmailMessage

def send_email(filepath):
    # Setup SMTP connection using config values stored by Hermes
    # In a real environment, you'd use a library to fetch these cleanly.
    host = "sandbox.smtp.mailtrap.io"
    port = 2525
    user = "708b2104a223afb78b36090cb0464bc6"
    pw = "708b2104a223afb78b36090cb0464bc6"

    with open(filepath, 'r') as f:
        content = f.read()

    msg = EmailMessage()
    msg['Subject'] = 'Diagnostic Couleur/Soin - Wella Professionals'
    msg['From'] = 'ai-sales@orchestra.com'
    msg['To'] = 'contact@celestine.fr'
    msg.set_content(content)

    with smtplib.SMTP(host, port) as server:
        server.login(user, pw)
        server.send_message(msg)

if __name__ == "__main__":
    send_email(sys.argv[1])
