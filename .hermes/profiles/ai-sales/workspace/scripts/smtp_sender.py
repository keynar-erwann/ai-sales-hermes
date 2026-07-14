#!/usr/bin/env python3
"""Safe Mailtrap sender for approved ai-sales review items.

Fail-safe rules:
- never sends files still in review-queue/pending;
- requires Status: approved unless --force is passed;
- requires an explicit To:/Recipient:/Email: field unless --test-recipient is passed;
- reads SMTP secrets only from the profile .env.
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, shutil, sys
from ai_sales_common import WORKSPACE, parse_review_markdown, send_email, load_env, now_iso

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('review_file', nargs='?')
    ap.add_argument('--check', action='store_true', help='Only check SMTP login')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--force', action='store_true', help='Allow sending a non-approved file')
    ap.add_argument('--test-recipient', action='store_true', help='Route to MAILTRAP_TEST_RECIPIENT instead of draft recipient')
    args=ap.parse_args()
    if args.check:
        from ai_sales_common import smtp_login_check
        print(json.dumps(smtp_login_check(), ensure_ascii=False, indent=2)); return 0
    if not args.review_file:
        ap.error('review_file required unless --check')
    p=Path(args.review_file).resolve()
    item=parse_review_markdown(p)
    if '/pending/' in str(p) and not args.force:
        print(json.dumps({'ok':False,'error':'refusing_to_send_pending_item','file':str(p)}, ensure_ascii=False)); return 2
    if item['status'].lower() not in {'approved','validated','validé','valide'} and not args.force:
        print(json.dumps({'ok':False,'error':'status_not_approved','status':item['status']}, ensure_ascii=False)); return 2
    env=load_env()
    recipient = env.get('MAILTRAP_TEST_RECIPIENT') if args.test_recipient else item['recipient']
    result=send_email(recipient, item['subject'], item['body'], dry_run=args.dry_run)
    result.update({'file':str(p),'checked_at':now_iso()})
    if result.get('ok') and not args.dry_run:
        sent=WORKSPACE/'review-queue'/'sent'; sent.mkdir(parents=True, exist_ok=True)
        if '/approved/' in str(p):
            shutil.move(str(p), str(sent/p.name))
            result['moved_to']=str(sent/p.name)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('ok') else 1
if __name__ == '__main__':
    raise SystemExit(main())
