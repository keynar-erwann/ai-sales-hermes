#!/usr/bin/env python3
from pathlib import Path
import json, re, sys, urllib.request, urllib.parse
from ai_sales_common import PROFILE_HOME, WORKSPACE, load_env, smtp_login_check

def slack_auth():
    env=load_env(); out={}
    tok=env.get('SLACK_BOT_TOKEN',''); app=env.get('SLACK_APP_TOKEN','')
    if tok:
        req=urllib.request.Request('https://slack.com/api/auth.test', data=b'', headers={'Authorization':'Bearer '+tok})
        try:
            r=json.loads(urllib.request.urlopen(req, timeout=20).read()); out['bot_ok']=r.get('ok'); out['bot_error']=r.get('error'); out['team']=r.get('team'); out['user']=r.get('user')
        except Exception as e: out['bot_ok']=False; out['bot_error']=type(e).__name__
    else: out['bot_ok']=False; out['bot_error']='missing'
    if app:
        req=urllib.request.Request('https://slack.com/api/apps.connections.open', data=b'', headers={'Authorization':'Bearer '+app})
        try:
            r=json.loads(urllib.request.urlopen(req, timeout=20).read()); out['socket_ok']=r.get('ok'); out['socket_error']=r.get('error')
        except Exception as e: out['socket_ok']=False; out['socket_error']=type(e).__name__
    else: out['socket_ok']=False; out['socket_error']='missing'
    return out

def main():
    required_skills=['icp-builder','prospect-discovery','signal-detection','pain-mapping','lead-enrichment','lead-scoring','message-personalization','linkedin-outreach','instagram-outreach','email-sequencing','reply-triage','objection-handling','meeting-scheduler','followup-cadence','handoff-brief','marketing-audit','personalized-offer','crm-sync','daily-orchestration','pipeline-report']
    skills={s:(PROFILE_HOME/'skills'/'ai-sales'/s/'SKILL.md').exists() for s in required_skills}
    docs={
        'challenge': (WORKSPACE/'CHALLENGE.md').exists(),
        'checklist': (WORKSPACE/'challenge-checklist.md').exists(),
        'soul': (PROFILE_HOME/'SOUL.md').exists(),
        'workspace_readme': (WORKSPACE/'README.md').exists(),
        'teams': (WORKSPACE/'company'/'teams.md').exists(),
        'handoffs': (WORKSPACE/'company'/'handoffs.md').exists(),
        'operating_model': (WORKSPACE/'company'/'operating-model.md').exists(),
    }
    dirs={d: (WORKSPACE/d).exists() for d in ['crm','review-queue/pending','review-queue/approved','review-queue/sent','reports','team-1-prospection-intelligence','team-2-outreach-engagement','team-3-admin-rdv','team-4-content-marketing','team-5-crm-orchestration']}
    config_text=(PROFILE_HOME/'config.yaml').read_text(errors='ignore')
    script_text='\n'.join(p.read_text(errors='ignore') for p in (WORKSPACE/'scripts').glob('*.py'))
    # Avoid exact secret values in config/scripts; env is allowed.
    env=load_env(); leaked=[]
    for k in ['SMTP_PASSWORD','SMTP_USER','SLACK_BOT_TOKEN','SLACK_APP_TOKEN']:
        v=env.get(k,'')
        if v and len(v)>8:
            if v in config_text: leaked.append(f'config:{k}')
            if v in script_text: leaked.append(f'script:{k}')
    result={
        'docs': docs,
        'team_dirs': dirs,
        'skills': skills,
        'all_required_skills_present': all(skills.values()),
        'smtp': smtp_login_check(),
        'slack': slack_auth(),
        'secret_leaks_outside_env': leaked,
        'pending_review_count': len(list((WORKSPACE/'review-queue'/'pending').glob('*.md'))),
        'approved_count': len(list((WORKSPACE/'review-queue'/'approved').glob('*.md'))),
    }
    result['core_local_ok'] = all(docs.values()) and all(dirs.values()) and all(skills.values()) and result['smtp'].get('ok') and result['slack'].get('bot_ok') and not leaked
    result['full_gateway_ok'] = bool(result['core_local_ok'] and result['slack'].get('socket_ok'))
    result['ok'] = result['full_gateway_ok']
    result['external_blockers'] = []
    if not result['slack'].get('socket_ok'):
        result['external_blockers'].append('SLACK_APP_TOKEN invalid for Socket Mode; create an app-level xapp token with connections:write in Slack and restart gateway')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['core_local_ok'] else 1
if __name__=='__main__': raise SystemExit(main())
