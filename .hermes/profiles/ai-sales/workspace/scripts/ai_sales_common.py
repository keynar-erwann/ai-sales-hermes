#!/usr/bin/env python3
"""Shared helpers for the ai-sales local-first challenge workflows."""
from __future__ import annotations
from pathlib import Path
import os, re, json, shutil, smtplib, ssl, urllib.parse, urllib.request
from email.message import EmailMessage
from datetime import datetime, timezone

PROFILE_HOME = Path(os.getenv("AI_SALES_PROFILE_HOME", "/root/.hermes/profiles/ai-sales"))
WORKSPACE = PROFILE_HOME / "workspace"
ENV_PATH = PROFILE_HOME / ".env"

def load_env() -> dict:
    vals = {}
    if ENV_PATH.exists():
        for raw in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            vals[k.strip()] = v.strip().strip('"').strip("'")
    for k, v in vals.items():
        os.environ.setdefault(k, v)
    return {**vals, **os.environ}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def parse_review_markdown(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    title = re.search(r"^#\s+(.+)$", text, re.M)
    status = re.search(r"^Status:\s*(.+)$", text, re.M|re.I)
    risk = re.search(r"^Risk:\s*(.+)$", text, re.M|re.I)
    signal = re.search(r"^Signal source:\s*(.+)$", text, re.M|re.I)
    to = re.search(r"^(?:To|Recipient|Email):\s*(\S+@\S+)$", text, re.M|re.I)
    obj = re.search(r"^Objet\s*:\s*(.+)$", text, re.M|re.I)
    body_match = re.search(r"## Email draft\s*\n(.*?)(?:\n## |\Z)", text, re.S|re.I)
    body = body_match.group(1).strip() if body_match else text.strip()
    # Remove subject line from body if present.
    body = re.sub(r"^Objet\s*:\s*.+\n+", "", body, flags=re.I).strip()
    return {
        "path": str(path),
        "filename": path.name,
        "title": title.group(1).strip() if title else path.stem,
        "status": status.group(1).strip() if status else "manual_review",
        "risk": risk.group(1).strip() if risk else "unknown",
        "signal_source": signal.group(1).strip() if signal else "",
        "recipient": to.group(1).strip() if to else "",
        "subject": obj.group(1).strip() if obj else f"Proposition personnalisée — {path.stem}",
        "body": body,
        "raw": text,
    }

def slack_post(text: str, *, blocks=None, channel: str|None=None) -> dict:
    env = load_env()
    token = env.get("SLACK_BOT_TOKEN", "")
    channel = channel or env.get("SLACK_CHANNEL_ID") or env.get("SLACK_HOME_CHANNEL")
    if not token or not channel:
        return {"ok": False, "error": "missing_slack_token_or_channel"}
    payload = {"channel": channel, "text": text}
    if blocks:
        payload["blocks"] = blocks
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"},
    )
    try:
        res = json.loads(urllib.request.urlopen(req, timeout=20).read())
        return res
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"}

def smtp_login_check() -> dict:
    env=load_env()
    required=["SMTP_HOST","SMTP_PORT","SMTP_USER","SMTP_PASSWORD"]
    missing=[k for k in required if not env.get(k)]
    if missing:
        return {"ok": False, "error": "missing_"+",".join(missing)}
    try:
        with smtplib.SMTP(env["SMTP_HOST"], int(env["SMTP_PORT"]), timeout=20) as s:
            s.ehlo()
            try:
                s.starttls(context=ssl.create_default_context()); s.ehlo()
            except Exception:
                pass
            code, _ = s.login(env["SMTP_USER"], env["SMTP_PASSWORD"])
        return {"ok": code == 235, "code": code}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"}

def send_email(recipient: str, subject: str, body: str, *, dry_run=False) -> dict:
    env=load_env()
    if dry_run:
        return {"ok": True, "dry_run": True, "recipient": recipient, "subject": subject}
    if not recipient or "@" not in recipient:
        return {"ok": False, "error": "missing_or_invalid_recipient"}
    msg=EmailMessage()
    msg["Subject"]=subject
    msg["From"]=env.get("MAILTRAP_FROM", "ai-sales@orchestra.local")
    msg["To"]=recipient
    msg.set_content(body)
    try:
        with smtplib.SMTP(env["SMTP_HOST"], int(env["SMTP_PORT"]), timeout=30) as s:
            s.ehlo()
            try:
                s.starttls(context=ssl.create_default_context()); s.ehlo()
            except Exception:
                pass
            s.login(env["SMTP_USER"], env["SMTP_PASSWORD"])
            s.send_message(msg)
        return {"ok": True, "recipient": recipient, "subject": subject}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"}
