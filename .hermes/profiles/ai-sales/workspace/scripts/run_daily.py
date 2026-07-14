#!/usr/bin/env python3
"""Daily orchestration loop for the ai-sales Hermes profile.

Default behavior is safe and challenge-aligned: inspect CRM/review queue, notify Slack,
write a report, and DO NOT send cold outreach. Use --send-approved only for files the
human moved to review-queue/approved.
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, subprocess, sys
from ai_sales_common import WORKSPACE, slack_post, smtp_login_check, now_iso
from review_manager import PENDING, APPROVED, list_items, notify_one

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--send-approved', action='store_true', help='Send only files already approved by a human')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--test-recipient', action='store_true', help='Route approved sends to MAILTRAP_TEST_RECIPIENT')
    ap.add_argument('--no-slack', action='store_true')
    args=ap.parse_args()

    pending=list_items(PENDING); approved=list_items(APPROVED)
    smtp=smtp_login_check()
    notifications=[] if args.no_slack else [notify_one(Path(i['path'])) for i in pending]
    sends=[]
    if args.send_approved:
        cmd=[sys.executable, str(WORKSPACE/'scripts'/'review_manager.py'), 'send-approved']
        if args.dry_run: cmd.append('--dry-run')
        if args.test_recipient: cmd.append('--test-recipient')
        cp=subprocess.run(cmd, text=True, capture_output=True)
        try: sends=json.loads(cp.stdout)
        except Exception: sends=[{'ok':False,'stdout':cp.stdout,'stderr':cp.stderr,'returncode':cp.returncode}]

    report={
        'checked_at': now_iso(),
        'challenge_mode': 'proof_bound_human_review_first',
        'smtp_login_ok': smtp.get('ok'),
        'pending_count': len(pending),
        'approved_count': len(approved),
        'slack_notifications': notifications,
        'send_approved_requested': args.send_approved,
        'send_results': sends,
        'next_action': 'Human must approve/reject pending drafts; only approved files can be sent.'
    }
    reports=WORKSPACE/'reports'; reports.mkdir(parents=True, exist_ok=True)
    out=reports/(now_iso()[:10]+'-daily-orchestration.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    md=reports/(now_iso()[:10]+'-daily-digest.md')
    md.write_text(f"# Daily digest — ai-sales\n\n- Pending review: {len(pending)}\n- Approved ready to send: {len(approved)}\n- SMTP login: {'OK' if smtp.get('ok') else 'KO'}\n- Slack notifications: {sum(1 for n in notifications if n.get('slack_ok'))}/{len(notifications)}\n- Envoi automatique: {'approved-only demandé' if args.send_approved else 'désactivé par défaut'}\n\nFichier JSON: `{out}`\n", encoding='utf-8')
    if not args.no_slack:
        slack_post(f"📊 *Digest ai-sales*\nPending review: {len(pending)}\nApproved: {len(approved)}\nSMTP: {'OK' if smtp.get('ok') else 'KO'}\nReport: {out}")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if smtp.get('ok') else 1
if __name__ == '__main__':
    raise SystemExit(main())
