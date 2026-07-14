#!/usr/bin/env python3
"""Human review queue manager for the ai-sales challenge profile."""
from __future__ import annotations
from pathlib import Path
import argparse, json, shutil, subprocess, sys
from ai_sales_common import WORKSPACE, parse_review_markdown, slack_post, now_iso

QUEUE=WORKSPACE/'review-queue'
PENDING=QUEUE/'pending'; APPROVED=QUEUE/'approved'; REJECTED=QUEUE/'rejected'; NOTIFIED=QUEUE/'notified'
for d in [PENDING, APPROVED, REJECTED, NOTIFIED]: d.mkdir(parents=True, exist_ok=True)

def list_items(folder: Path) -> list[dict]:
    return [parse_review_markdown(p) for p in sorted(folder.glob('*.md'))]

def notify_one(p: Path) -> dict:
    item=parse_review_markdown(p)
    text=(f"🔎 *Validation outreach requise* — `{p.name}`\n"
          f"Status: {item['status']} · Risk: {item['risk']}\n"
          f"Signal: {item['signal_source'] or 'non renseigné'}\n"
          f"Objet: {item['subject']}\n\n"
          f"Action locale sûre: `python3 workspace/scripts/review_manager.py approve {p.name}` puis `run_daily.py --send-approved`.\n"
          f"Aucun envoi ne part tant que le fichier reste dans pending/.")
    res=slack_post(text)
    marker=NOTIFIED/(p.name+'.json')
    marker.write_text(json.dumps({'file':str(p),'slack':res,'at':now_iso()}, ensure_ascii=False, indent=2), encoding='utf-8')
    return {'file':p.name,'slack_ok':res.get('ok'), 'slack_error':res.get('error')}

def move(name: str, dst: Path, status: str) -> dict:
    src=PENDING/name
    if not src.exists():
        src=APPROVED/name
    if not src.exists():
        return {'ok':False,'error':'file_not_found','name':name}
    text=src.read_text(encoding='utf-8', errors='ignore')
    if 'Status:' in text:
        text=__import__('re').sub(r'^Status:\s*.*$', f'Status: {status}', text, flags=__import__('re').M)
    else:
        text=f'Status: {status}\n'+text
    dst.mkdir(parents=True, exist_ok=True)
    target=dst/name
    src.write_text(text, encoding='utf-8')
    shutil.move(str(src), str(target))
    return {'ok':True,'from':str(src),'to':str(target),'status':status}

def main() -> int:
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('list')
    sub.add_parser('notify')
    a=sub.add_parser('approve'); a.add_argument('filename')
    r=sub.add_parser('reject'); r.add_argument('filename')
    s=sub.add_parser('send-approved'); s.add_argument('--dry-run', action='store_true'); s.add_argument('--test-recipient', action='store_true')
    args=ap.parse_args()
    if args.cmd=='list':
        print(json.dumps({'pending':list_items(PENDING),'approved':list_items(APPROVED),'rejected':list_items(REJECTED)}, ensure_ascii=False, indent=2)); return 0
    if args.cmd=='notify':
        print(json.dumps([notify_one(p) for p in sorted(PENDING.glob('*.md'))], ensure_ascii=False, indent=2)); return 0
    if args.cmd=='approve':
        print(json.dumps(move(args.filename, APPROVED, 'approved'), ensure_ascii=False, indent=2)); return 0
    if args.cmd=='reject':
        print(json.dumps(move(args.filename, REJECTED, 'rejected'), ensure_ascii=False, indent=2)); return 0
    if args.cmd=='send-approved':
        results=[]
        for p in sorted(APPROVED.glob('*.md')):
            cmd=[sys.executable, str(WORKSPACE/'scripts'/'smtp_sender.py'), str(p)]
            if args.dry_run: cmd.append('--dry-run')
            if args.test_recipient: cmd.append('--test-recipient')
            cp=subprocess.run(cmd, text=True, capture_output=True)
            try: data=json.loads(cp.stdout)
            except Exception: data={'ok':False,'stdout':cp.stdout,'stderr':cp.stderr,'returncode':cp.returncode}
            results.append(data)
        print(json.dumps(results, ensure_ascii=False, indent=2)); return 0 if all(r.get('ok') for r in results) else 1
if __name__ == '__main__':
    raise SystemExit(main())
