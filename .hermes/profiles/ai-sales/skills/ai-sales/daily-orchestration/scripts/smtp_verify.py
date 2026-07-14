#!/usr/bin/env python3
import smtplib
import os
import sys
from email.message import EmailMessage

# This script is used by the daily-orchestration skill to verify
# SMTP connectivity before starting bulk outreach.
#
# Credentials are expected via environment variables, 
# falling back to sandbox defaults if not set.

SMTP_HOST = os.getenv("SMTP_HOST", "sandbox.smtp.mailtrap.io")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "50352554747535")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "708b2104a223afb78b36090cb0464bc6")

def test_smtp_connection():
    print(f"Testing SMTP connection to {SMTP_HOST}:{SMTP_PORT}...")
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.quit()
        print("Success: SMTP credentials valid.")
        return True
    except Exception as e:
        print(f"Failure: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if test_smtp_connection() else 1)
