#!/usr/bin/env python3
"""Small Hunter.io client for the ai-sales lead-enrichment skill.

Reads HUNTER_API_KEY from the environment. Never pass the API key on the
command line, because shell history and process listings can leak it.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

API_BASE = "https://api.hunter.io/v2"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def fail(message: str, code: int = 1) -> None:
    print(json.dumps({"ok": False, "error": message, "checked_at": iso_now()}, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def load_dotenv_key() -> str:
    """Fallback loader for direct shell use outside a Hermes ai-sales session."""
    env_path = "/root/.hermes/profiles/ai-sales/.env"
    try:
        with open(env_path, "r", encoding="utf-8") as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                name, value = stripped.split("=", 1)
                if name.strip() == "HUNTER_API_KEY":
                    return value.strip().strip('"').strip("'")
    except FileNotFoundError:
        return ""
    return ""


def get_api_key() -> str:
    key = os.getenv("HUNTER_API_KEY", "").strip() or load_dotenv_key()
    if not key:
        fail("HUNTER_API_KEY is missing. Add it to /root/.hermes/profiles/ai-sales/.env as HUNTER_API_KEY=...", 2)
    return key


def request(endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    key = get_api_key()
    clean_params = {k: v for k, v in params.items() if v is not None and v != ""}
    clean_params["api_key"] = key
    url = f"{API_BASE}/{endpoint}?{urllib.parse.urlencode(clean_params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-ai-sales-hunter-client/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            data = json.loads(raw) if raw else {}
            return {"http_status": resp.status, "response": data}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            body = {"raw": raw[:1000]}
        return {"http_status": exc.code, "response": body}
    except urllib.error.URLError as exc:
        fail(f"Network error calling Hunter.io: {exc}", 3)
    except TimeoutError:
        fail("Timeout calling Hunter.io", 3)


def emit(operation: str, params: dict[str, Any], result: dict[str, Any], raw: bool = False) -> None:
    # Never echo api_key. Only include safe request params.
    safe_params = {k: v for k, v in params.items() if k != "api_key" and v is not None and v != ""}
    response = result.get("response", {})
    ok = 200 <= int(result.get("http_status", 0)) < 300
    payload: dict[str, Any] = {
        "ok": ok,
        "operation": operation,
        "request": safe_params,
        "http_status": result.get("http_status"),
        "checked_at": iso_now(),
    }
    if raw:
        payload["hunter_response"] = response
    else:
        payload.update(normalize(operation, response))
        if not ok:
            payload["hunter_error"] = response.get("errors") or response.get("error") or response
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(4)


def normalize(operation: str, response: dict[str, Any]) -> dict[str, Any]:
    data = response.get("data") if isinstance(response, dict) else None
    if not isinstance(data, dict):
        return {"data": data}

    if operation == "domain-search":
        emails = data.get("emails") or []
        return {
            "company": {
                "domain": data.get("domain"),
                "organization": data.get("organization"),
                "pattern": data.get("pattern"),
            },
            "emails": [summarize_email(e) for e in emails],
            "count": len(emails),
        }

    if operation == "email-finder":
        return {
            "email": {
                "address": data.get("email"),
                "status": contactability_from_finder(data),
                "hunter_score": data.get("score"),
                "sources": data.get("sources") or [],
            },
            "person": {
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "position": data.get("position"),
                "company": data.get("company"),
                "linkedin_url": data.get("linkedin_url"),
                "twitter": data.get("twitter"),
                "phone_number": data.get("phone_number"),
            },
        }

    if operation == "email-verifier":
        return {
            "email": {
                "address": data.get("email"),
                "status": contactability_from_verifier(data),
                "hunter_score": data.get("score"),
                "result": data.get("result"),
                "regexp": data.get("regexp"),
                "gibberish": data.get("gibberish"),
                "disposable": data.get("disposable"),
                "webmail": data.get("webmail"),
                "mx_records": data.get("mx_records"),
                "smtp_server": data.get("smtp_server"),
                "smtp_check": data.get("smtp_check"),
                "accept_all": data.get("accept_all"),
                "block": data.get("block"),
                "sources": data.get("sources") or [],
            }
        }

    if operation == "account":
        # Account info is useful for testing key validity and quota, but keep it compact.
        return {"account": data}

    return {"data": data}


def summarize_email(e: dict[str, Any]) -> dict[str, Any]:
    return {
        "address": e.get("value"),
        "type": e.get("type"),
        "confidence": e.get("confidence"),
        "first_name": e.get("first_name"),
        "last_name": e.get("last_name"),
        "position": e.get("position"),
        "linkedin_url": e.get("linkedin"),
        "phone_number": e.get("phone_number"),
        "sources": e.get("sources") or [],
    }


def contactability_from_finder(data: dict[str, Any]) -> str:
    email = data.get("email")
    score = data.get("score")
    if not email:
        return "not_found"
    if isinstance(score, int | float):
        if score >= 80:
            return "probable"
        if score >= 50:
            return "risky"
    return "probable"


def contactability_from_verifier(data: dict[str, Any]) -> str:
    result = str(data.get("result") or "").lower()
    score = data.get("score")
    if data.get("disposable") or data.get("webmail"):
        return "not_contactable"
    if result == "deliverable" and isinstance(score, int | float) and score >= 80:
        return "verified"
    if result == "deliverable":
        return "probable"
    if result in {"undeliverable", "invalid"}:
        return "not_contactable"
    return "risky"


def split_csv_urls(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def build_lead_record(args: argparse.Namespace) -> dict[str, Any]:
    """Build a CRM/outreach-ready lead record using finder + verifier.

    This intentionally spends one Hunter search and, when an email is found,
    one Hunter verification. It returns a safe next action rather than sending.
    """
    checked_at = iso_now()
    finder_params = {
        "domain": args.domain,
        "first_name": args.first_name,
        "last_name": args.last_name,
        "company": args.company,
    }
    finder_result = request("email-finder", finder_params)
    finder_ok = 200 <= int(finder_result.get("http_status", 0)) < 300
    finder_data = finder_result.get("response", {}).get("data") if isinstance(finder_result.get("response"), dict) else None
    if not isinstance(finder_data, dict):
        finder_data = {}

    email_address = finder_data.get("email")
    verifier_result: dict[str, Any] | None = None
    verifier_data: dict[str, Any] = {}
    if finder_ok and email_address:
        verifier_result = request("email-verifier", {"email": email_address})
        raw_verifier_data = verifier_result.get("response", {}).get("data") if isinstance(verifier_result.get("response"), dict) else None
        if isinstance(raw_verifier_data, dict):
            verifier_data = raw_verifier_data

    email_status = "not_found"
    if email_address and verifier_data:
        email_status = contactability_from_verifier(verifier_data)
    elif email_address:
        email_status = contactability_from_finder(finder_data)

    sources = verifier_data.get("sources") or finder_data.get("sources") or []
    next_action = "manual_review" if email_status in {"verified", "probable"} else "research_more"
    if email_status in {"risky", "not_contactable"}:
        next_action = "manual_review" if email_status == "risky" else "discard"

    title = args.title or finder_data.get("position") or ""
    linkedin_url = args.linkedin_url or finder_data.get("linkedin_url") or ""
    company_name = args.company or finder_data.get("company") or ""

    notes: list[str] = []
    if not finder_ok:
        notes.append("Hunter.io email-finder did not return a successful HTTP response.")
    if not email_address:
        notes.append("No email returned by Hunter.io email-finder; do not guess an email pattern.")
    if email_address and not verifier_data:
        notes.append("Email was found but verifier did not return usable verification data; keep status conservative.")
    if email_status in {"verified", "probable"}:
        notes.append("Cold outreach still requires human validation before sending.")

    record = {
        "ok": finder_ok and (not email_address or bool(verifier_data)),
        "operation": "lead-record",
        "company": {
            "name": company_name,
            "domain": args.domain,
            "source_urls": split_csv_urls(args.company_source_urls),
        },
        "person": {
            "first_name": finder_data.get("first_name") or args.first_name,
            "last_name": finder_data.get("last_name") or args.last_name,
            "title": title,
            "linkedin_url": linkedin_url,
            "source_urls": split_csv_urls(args.person_source_urls),
        },
        "email": {
            "address": email_address or "",
            "status": email_status,
            "hunter_score": verifier_data.get("score") if verifier_data else finder_data.get("score"),
            "hunter_finder": {
                "http_status": finder_result.get("http_status"),
                "score": finder_data.get("score"),
                "sources": finder_data.get("sources") or [],
            },
            "hunter_verification": verifier_data,
            "hunter_sources": sources,
        },
        "proof": {
            "tools_used": ["hunter.io"],
            "checked_at": checked_at,
            "notes": notes,
        },
        "next_action": next_action,
    }
    if verifier_result is not None:
        record["email"]["hunter_verifier_http_status"] = verifier_result.get("http_status")
    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hunter.io client for ai-sales lead enrichment. Outputs JSON and never prints the API key.")
    parser.add_argument("--raw", action="store_true", help="include raw Hunter.io response body")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("account", help="check API key/quota")

    p = sub.add_parser("domain-search", help="find contacts and email pattern for a company domain")
    p.add_argument("--domain", required=True)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--department")
    p.add_argument("--seniority")
    p.add_argument("--type", choices=["personal", "generic"])

    p = sub.add_parser("email-finder", help="find a professional email for a named person at a domain")
    p.add_argument("--domain", required=True)
    p.add_argument("--first-name", required=True)
    p.add_argument("--last-name", required=True)
    p.add_argument("--company")

    p = sub.add_parser("email-verifier", help="verify an email before CRM/outreach handoff")
    p.add_argument("--email", required=True)

    p = sub.add_parser("lead-record", help="build a proof-backed lead record with email-finder + verifier")
    p.add_argument("--domain", required=True)
    p.add_argument("--first-name", required=True)
    p.add_argument("--last-name", required=True)
    p.add_argument("--company", help="company name, e.g. Stripe")
    p.add_argument("--title", help="known role/title from a public source or prior discovery")
    p.add_argument("--linkedin-url", help="known LinkedIn profile URL from a public source or Hunter.io")
    p.add_argument("--company-source-urls", help="comma-separated source URLs proving company/domain context")
    p.add_argument("--person-source-urls", help="comma-separated source URLs proving person/title/company context")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    raw = bool(args.raw)

    if args.command == "account":
        params: dict[str, Any] = {}
        result = request("account", params)
        emit("account", params, result, raw=raw)
        return 0

    if args.command == "domain-search":
        params = {
            "domain": args.domain,
            "limit": args.limit,
            "offset": args.offset,
            "department": args.department,
            "seniority": args.seniority,
            "type": args.type,
        }
        result = request("domain-search", params)
        emit("domain-search", params, result, raw=raw)
        return 0

    if args.command == "email-finder":
        params = {
            "domain": args.domain,
            "first_name": args.first_name,
            "last_name": args.last_name,
            "company": args.company,
        }
        result = request("email-finder", params)
        emit("email-finder", params, result, raw=raw)
        return 0

    if args.command == "email-verifier":
        params = {"email": args.email}
        result = request("email-verifier", params)
        emit("email-verifier", params, result, raw=raw)
        return 0

    if args.command == "lead-record":
        if raw:
            fail("--raw is not supported for lead-record; use email-finder/email-verifier separately for raw Hunter.io responses.", 2)
        record = build_lead_record(args)
        print(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if record.get("ok") else 4

    fail(f"Unknown command: {args.command}", 2)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
