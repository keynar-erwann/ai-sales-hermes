from pathlib import Path
import json, csv, re, hashlib
from datetime import datetime, timezone

BASE = Path('/root/.hermes/profiles/ai-sales')
WS = BASE / 'workspace'
RUN = WS / 'prospect-runs' / '2026-07-12-wella-professionals-fr'
SK = BASE / 'skills' / 'ai-sales'
NOW = datetime.now(timezone.utc).isoformat()

leads = json.loads((RUN / 'discovery.json').read_text(encoding='utf-8'))

def slug(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')[:60] or hashlib.sha1(s.encode()).hexdigest()[:8]

# 1) CRM sync local
accounts=[]; contacts=[]; opps=[]; interactions=[]
for i,c in enumerate(leads,1):
    account_id = 'acct_' + slug(c['company']['domain'] or c['company']['name'])
    contact_id = 'cont_' + slug(c['company']['name']) + '_role'
    opp_id = 'opp_wella_' + slug(c['company']['name'])
    stage = 'qualified' if c['score']['total'] >= 4.0 else 'candidate'
    next_action = 'identify_decision_maker' if c['email']['status']=='not_found' else c['next_action']
    accounts.append({
        'account_id': account_id,
        'name': c['company']['name'],
        'domain': c['company']['domain'],
        'website': c['company']['website'],
        'city': c['company']['city'],
        'address': c['company'].get('address',''),
        'segment': c['company']['segment'],
        'source_urls': c['company']['source_urls'],
        'stage': stage,
        'score_total': c['score']['total'],
        'next_action': next_action,
        'created_at': NOW,
        'updated_at': NOW
    })
    contacts.append({
        'contact_id': contact_id,
        'account_id': account_id,
        'first_name': '',
        'last_name': '',
        'title': c['person']['title'],
        'email': '',
        'email_status': c['email']['status'],
        'linkedin_url': '',
        'source_urls': c['person']['source_urls'],
        'notes': 'Personne nommée non identifiée ; ne pas deviner. Cibler propriétaire/directeur artistique après recherche manuelle.',
        'created_at': NOW,
        'updated_at': NOW
    })
    opps.append({
        'opportunity_id': opp_id,
        'account_id': account_id,
        'partner': 'Wella Professionals France',
        'hypothesis': c['pain_hypothesis'],
        'signal': c['signal'],
        'stage': 'qualified_research_needed' if stage=='qualified' else 'candidate',
        'score': c['score'],
        'next_action': next_action,
        'created_at': NOW,
        'updated_at': NOW
    })
    interactions.append({
        'interaction_id': 'int_' + hashlib.sha1((account_id+NOW).encode()).hexdigest()[:12],
        'account_id': account_id,
        'contact_id': contact_id,
        'type': 'crm_import',
        'summary': f"Lead importé depuis le run Wella avec score {c['score']['total']} et statut email {c['email']['status']}.",
        'source': str(RUN / 'discovery.json'),
        'created_at': NOW
    })

for name,data in [('accounts.json',accounts),('contacts.json',contacts),('opportunities.json',opps),('interactions.json',interactions)]:
    (WS/'crm'/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
if not (WS/'crm'/'opt_outs.json').exists():
    (WS/'crm'/'opt_outs.json').write_text('[]\n', encoding='utf-8')

# 2) Review queue drafts for top 5
pending = WS / 'review-queue' / 'pending'
pending.mkdir(parents=True, exist_ok=True)
outreach_dir = WS / 'outreach-drafts'
outreach_dir.mkdir(parents=True, exist_ok=True)
review_files=[]
for c in leads[:5]:
    account = c['company']['name']; s=slug(account)
    angle = f"Le site met en avant {c['signal']['summary'].split(';')[0].replace('services/mentions ', '')}. L'angle Wella : fiabilité couleur/soin + support technique pour renforcer une prestation déjà visible."
    email = f"""Bonjour,\n\nJ’ai vu que {account} met déjà en avant des prestations autour de {c['signal']['summary'].split(':')[-1].split(';')[0].strip()}.\n\nC’est précisément le type de salon où Wella Professionals peut avoir du sens : aider l’équipe à sécuriser des résultats couleur/soin constants, tout en gardant un positionnement premium.\n\nEst-ce que cela vaudrait le coup de vous partager une idée courte de diagnostic couleur/soin adaptée à votre salon ?\n\nBien à vous,"""
    md = f"""# Review Item — {account}\n\nStatus: manual_review\nRisk: medium\nReason risk: décideur et email non identifiés ; draft préparé mais non envoyable.\nLead source: {c['company']['source_urls'][0]}\nSignal source: {c['signal']['source_url']}\n\n## Angle\n\n{angle}\n\n## Email draft\n\n{email}\n\n## LinkedIn draft optionnel\n\nBonjour, j’ai remarqué le positionnement couleur/soin de {account}. Je travaille sur une piste Wella Professionals autour de la régularité des résultats couleur et du support technique salon. Ouvert(e) à ce que je vous partage l’idée en 3 lignes ?\n\n## Pourquoi c'est personnalisé\n\n- Signal utilisé : {c['signal']['summary']}\n- Hypothèse : {c['pain_hypothesis']}\n- Source : {c['signal']['source_url']}\n\n## Décision humaine requise\n\n- Identifier le bon décideur.\n- Vérifier l'email professionnel ou choisir un canal conforme.\n- Valider que l'angle Wella est pertinent.\n"""
    path = pending / f"wella-{s}.md"
    path.write_text(md, encoding='utf-8')
    review_files.append(str(path))
    (outreach_dir / f"wella-{s}.md").write_text(md, encoding='utf-8')

# 3) Content audits and offers for top 3
audits_dir = WS / 'content-assets' / 'audits'; offers_dir = WS / 'content-assets' / 'offers'
audits_dir.mkdir(parents=True, exist_ok=True); offers_dir.mkdir(parents=True, exist_ok=True)
for c in leads[:3]:
    s=slug(c['company']['name'])
    audit = f"""# Audit express — {c['company']['name']}\n\nPartner: Wella Professionals France\nSource principale: {c['signal']['source_url']}\n\n## Observation sourcée\n\n{c['signal']['summary']}\n\n## Lecture commerciale\n\nLe salon montre déjà des signaux compatibles avec une offre professionnelle couleur/soin. L'opportunité n'est pas d'envoyer un message générique, mais de proposer un diagnostic court sur la régularité des résultats couleur, l'entretien soin et la valorisation des transformations.\n\n## Hypothèse de douleur\n\n{c['pain_hypothesis']}\n\n## Angle Wella\n\nPositionner Wella comme partenaire technique : couleur salon, soin associé, support pour maintenir une expérience premium.\n\n## Prochaine action\n\nPréparer un message `manual_review`, puis identifier un décideur nommé avant tout enrichissement email.\n"""
    offer = f"""# One-pager d'offre — {c['company']['name']} x Wella Professionals\n\n## Proposition\n\nDiagnostic couleur & soin en salon : identifier les prestations couleur fortes, les opportunités d'entretien soin, et la manière de transformer ces services en expérience premium récurrente.\n\n## Pourquoi ce salon\n\nSignal public : {c['signal']['summary']}\n\n## Valeur proposée\n\n- Cohérence des résultats couleur.\n- Support technique autour coloration + soin.\n- Angle de contenu avant/après pour mieux vendre les prestations.\n- Possibilité de formation ou mini-masterclass si pertinent.\n\n## CTA doux\n\nProposer un échange court ou l'envoi d'un diagnostic en 3 points, sans automatiser l'outreach.\n"""
    (audits_dir / f"wella-{s}-audit.md").write_text(audit, encoding='utf-8')
    (offers_dir / f"wella-{s}-offer.md").write_text(offer, encoding='utf-8')

# 4) Meeting/handoff simulation
meetings = WS / 'meetings'; meetings.mkdir(parents=True, exist_ok=True)
top = leads[0]
(meetings/'wella-positive-reply-simulation.md').write_text(f"""# Simulation réponse positive — {top['company']['name']}\n\n## Réponse simulée\n\n« Bonjour, oui pourquoi pas, envoyez-nous quelques informations. »\n\n## Action Admin & RDV\n\nNe pas réserver automatiquement. Proposer 2-3 créneaux ou demander le bon interlocuteur.\n\n## Créneaux proposés\n\n- Mardi 10:00\n- Mercredi 14:30\n- Jeudi 11:30\n\n## Handoff brief\n\nCompte : {top['company']['name']}\nSite : {top['company']['website']}\nSignal : {top['signal']['summary']}\nHypothèse : {top['pain_hypothesis']}\nRisque : décideur/email non identifiés.\nProchaine étape : valider interlocuteur et proposer diagnostic couleur/soin Wella.\n""", encoding='utf-8')

# 5) Pipeline report + daily orchestration
reports = WS / 'reports'; reports.mkdir(parents=True, exist_ok=True)
stage_counts={}
for a in accounts: stage_counts[a['stage']]=stage_counts.get(a['stage'],0)+1
report = f"""# Pipeline Report — Wella Professionals France\n\nDate: 2026-07-12\n\n## Executive summary\n\nRun Wella produit avec {len(leads)} leads sélectionnés depuis {len(json.loads((RUN/'candidates.json').read_text(encoding='utf-8')))} candidats sauvegardés. Les leads sont sourcés via OpenStreetMap + sites publics. Aucun décideur ni email n'a été inventé.\n\n## Pipeline counts\n\n- Accounts CRM: {len(accounts)}\n- Contacts placeholder: {len(contacts)}\n- Opportunities: {len(opps)}\n- Review queue pending: {len(review_files)}\n- Content audits: 3\n- Offers: 3\n- Meetings simulated: 1\n\n## Stages\n\n{json.dumps(stage_counts, indent=2, ensure_ascii=False)}\n\n## Top 5 leads\n\n"""
for i,c in enumerate(leads[:5],1):
    report += f"{i}. {c['company']['name']} — {c['company']['city']} — score {c['score']['total']} — {c['signal']['source_url']}\n"
report += """
## Blockers\n\n- Décideurs nommés à rechercher avant Hunter.io.\n- Slack/Gmail/Resend/CRM externe non branchés ; la démo reste local-first.\n- Les signaux sont solides pour le positionnement, mais plusieurs ne sont pas des actualités datées.\n\n## Next actions by team\n\n- Équipe 1 Prospection: enrichir manuellement les décideurs des 5 meilleurs leads.\n- Équipe 2 Outreach: faire relire les 5 drafts en review queue.\n- Équipe 3 Admin: utiliser la simulation de réponse positive pour tester le handoff brief.\n- Équipe 4 Content: compléter audits/offers pour plus de comptes si nécessaire.\n- Équipe 5 CRM: valider le CRM local puis tester `daily-orchestration`.\n"""
(reports/'2026-07-12-wella-pipeline-report.md').write_text(report, encoding='utf-8')

digest = f"""# Daily Orchestration Digest — Wella Professionals France\n\nDate: 2026-07-12\n\n## Pipeline status\n\n- Partner brief: prêt.\n- ICP: prêt.\n- Discovery: {len(leads)} leads sélectionnés.\n- CRM local: {len(accounts)} accounts synchronisés.\n- Review queue: {len(review_files)} messages en attente.\n- Content assets: 3 audits + 3 offers.\n- Meeting flow: 1 simulation créée.\n\n## Team 1 — Prospection & Intelligence\n\nAction suivante : rechercher décideurs nommés pour les 5 meilleurs leads, puis seulement ensuite utiliser Hunter.io.\n\n## Team 2 — Outreach & Engagement\n\nAction suivante : validation humaine des drafts `workspace/review-queue/pending/`. Aucun envoi automatique.\n\n## Team 3 — Admin & Rendez-vous\n\nAction suivante : tester le handoff sur `workspace/meetings/wella-positive-reply-simulation.md`.\n\n## Team 4 — Content & Marketing\n\nAction suivante : enrichir les audits top 3 si la démo doit montrer la valeur avant la demande.\n\n## Team 5 — CRM & Orchestration\n\nAction suivante : utiliser le rapport pipeline pour piloter la prochaine itération.\n\n## Decisions needed from human\n\n- Confirmer que Wella Professionals France est bien le partenaire et non une autre entité “Wella Studio”.\n- Décider si on branche Slack/Gmail maintenant ou si la première démo reste local-first.\n- Valider ou corriger les messages avant tout envoi.\n"""
(reports/'2026-07-12-daily-orchestration-digest.md').write_text(digest, encoding='utf-8')
(WS/'demo'/'transcript.md').write_text(f"""# Demo Transcript — Wella local-first\n\n1. Brief Wella lu depuis `partner-brief-wella-professionals-fr.md`.\n2. ICP produit dans `{RUN/'icp.md'}`.\n3. Découverte produite : `{RUN/'discovery.json'}` et `{RUN/'discovery.csv'}`.\n4. CRM local synchronisé dans `workspace/crm/`.\n5. Review queue créée avec {len(review_files)} drafts.\n6. Content assets créés pour 3 comptes.\n7. Handoff meeting simulé.\n8. Pipeline report et daily digest générés.\n\nAucun email ou message externe n'a été envoyé.\n""", encoding='utf-8')

# 6) Missing secondary skill docs

def skill(name, desc, body, tags):
    return f"""---\nname: {name}\ndescription: \"{desc}\"\nversion: 1.0.0\nauthor: Hermes Agent\nlicense: MIT\nmetadata:\n  hermes:\n    tags: [{', '.join(tags)}]\n    related_skills: []\n---\n\n{body}\n"""

secondary = {
'signal-detection': ('Use when detecting and documenting recent or public trigger signals for AI Sales Company prospects before scoring and outreach.', '# Signal Detection\n\n## Overview\n\nFinds public, source-backed reasons why a prospect is worth contacting now or why the account is relevant.\n\n## Procedure\n\n1. Inspect website, news, social/public pages, job posts and reviews.\n2. Record the exact source URL.\n3. Classify the signal: hiring, launch, expansion, content, service focus, review pattern, training, or unknown.\n4. If no source exists, mark as hypothesis and route to `research_more`.\n\n## Verification Checklist\n\n- [ ] Every signal has a source URL.\n- [ ] Signal is separate from pain hypothesis.\n- [ ] Unsourced signals are not used in outreach.\n', ['sales','signals','ai-sales']),
'pain-mapping': ('Use when translating sourced prospect signals into cautious pain hypotheses for personalized outreach and scoring.', '# Pain Mapping\n\n## Overview\n\nTurns signals into useful hypotheses without pretending to know the prospect’s internal pain.\n\n## Procedure\n\n1. Start from a sourced signal.\n2. Map the likely business implication.\n3. Phrase as hypothesis, never fact.\n4. Connect only to a relevant partner value.\n\n## Verification Checklist\n\n- [ ] Pain is phrased as probable/hypothesis.\n- [ ] Pain traces to a signal.\n- [ ] No unsupported internal claims.\n', ['sales','pain-mapping','ai-sales']),
'email-sequencing': ('Use when preparing a safe multi-touch email sequence for manually approved AI Sales Company outreach.', '# Email Sequencing\n\n## Overview\n\nPrepares multi-touch email sequences. It does not send emails unless a compliant integration and human approval are present.\n\n## Procedure\n\n1. Use a personalized first email.\n2. Draft two light follow-ups.\n3. Preserve opt-out language.\n4. Save to review queue with `manual_review`.\n\n## Verification Checklist\n\n- [ ] First email uses a real signal.\n- [ ] Follow-ups add value, not pressure.\n- [ ] No sending without approval.\n', ['sales','email','ai-sales']),
'reply-triage': ('Use when classifying inbound replies into interested, objection, later, not-now, opt-out, or irrelevant, then routing CRM next actions.', '# Reply Triage\n\n## Overview\n\nClassifies replies and updates CRM routing.\n\n## Procedure\n\n1. Read reply and thread context.\n2. Classify: interested, objection, later, not_now, opt_out, irrelevant.\n3. Update CRM stage and interaction.\n4. Route to meeting, objection handling, follow-up, or hard stop.\n\n## Verification Checklist\n\n- [ ] Opt-outs are hard stops.\n- [ ] Positive replies route to Admin & RDV.\n- [ ] CRM interaction is recorded.\n', ['sales','reply-triage','ai-sales']),
'objection-handling': ('Use when drafting careful, human responses to prospect objections without overclaiming or pressuring.', '# Objection Handling\n\n## Overview\n\nDrafts responses to common objections while staying human and non-pushy.\n\n## Procedure\n\n1. Identify the objection.\n2. Acknowledge it plainly.\n3. Respond with one relevant proof or clarification.\n4. Offer a low-friction next step or close politely.\n\n## Verification Checklist\n\n- [ ] No pressure.\n- [ ] No unsupported claims.\n- [ ] Respect opt-outs and timing.\n', ['sales','objections','ai-sales']),
'meeting-scheduler': ('Use when turning a positive reply into proposed meeting slots, calendar-ready details, and CRM next actions.', '# Meeting Scheduler\n\n## Overview\n\nTransforms interest into a calendar-ready next step.\n\n## Procedure\n\n1. Confirm the right person and topic.\n2. Propose 2-3 slots or ask for availability.\n3. Add buffer/context notes.\n4. Update CRM.\n\n## Verification Checklist\n\n- [ ] No calendar action without approval/integration.\n- [ ] Meeting purpose is clear.\n- [ ] Handoff brief is triggered.\n', ['sales','calendar','ai-sales']),
'followup-cadence': ('Use when planning respectful follow-ups for silence, later, no-show, or post-meeting states.', '# Followup Cadence\n\n## Overview\n\nPlans follow-ups without spam or artificial urgency.\n\n## Procedure\n\n1. Read CRM stage and prior interaction.\n2. Choose cadence type: silence, later, no-show, post_meeting.\n3. Draft one concise next touch.\n4. Respect opt-outs.\n\n## Verification Checklist\n\n- [ ] Cadence matches stage.\n- [ ] Volume is conservative.\n- [ ] Opt-outs excluded.\n', ['sales','followup','ai-sales']),
'handoff-brief': ('Use when preparing a complete pre-meeting brief from CRM, sources, signals, and outreach history.', '# Handoff Brief\n\n## Overview\n\nPrepares context before a sales meeting.\n\n## Procedure\n\n1. Summarize account and contact.\n2. Include sources, signal, pain hypothesis and prior messages.\n3. List risks and unknowns.\n4. Suggest meeting objective and questions.\n\n## Verification Checklist\n\n- [ ] Sources included.\n- [ ] Unknowns explicit.\n- [ ] Brief is concise enough to use before a call.\n', ['sales','handoff','ai-sales']),
'marketing-audit': ('Use when creating a short, source-backed audit of a prospect website/social presence to support value-first outreach.', '# Marketing Audit\n\n## Overview\n\nCreates a value-first audit from public evidence.\n\n## Procedure\n\n1. Inspect website/social/source.\n2. Identify one strength and one opportunity.\n3. Connect to the partner offer.\n4. Save as an asset, not a sent message.\n\n## Verification Checklist\n\n- [ ] Audit cites sources.\n- [ ] No harsh/unproven criticism.\n- [ ] Clear next action.\n', ['sales','marketing','ai-sales']),
'personalized-offer': ('Use when turning a prospect audit and partner value proposition into a concise one-pager offer for manual review.', '# Personalized Offer\n\n## Overview\n\nCreates a one-pager offer tailored to a specific prospect.\n\n## Procedure\n\n1. Use a sourced audit.\n2. Pick one value proposition.\n3. Write a short offer and CTA.\n4. Save for review.\n\n## Verification Checklist\n\n- [ ] Offer is prospect-specific.\n- [ ] CTA is low pressure.\n- [ ] Claims are supported.\n', ['sales','offer','ai-sales']),
'linkedin-outreach': ('Use when preparing compliant LinkedIn outreach drafts and cadence notes without automating actions unless an approved integration is configured.', '# LinkedIn Outreach\n\n## Overview\n\nPrepares LinkedIn messages. It does not automate LinkedIn actions by default.\n\n## Procedure\n\n1. Verify the person/profile source.\n2. Draft a short connection or DM.\n3. Keep cadence conservative.\n4. Route to manual review or approved integration.\n\n## Verification Checklist\n\n- [ ] Profile is sourced.\n- [ ] No scraping or automation without approved tool.\n- [ ] Message is personalized.\n', ['sales','linkedin','ai-sales']),
'instagram-outreach': ('Use when preparing compliant Instagram DM drafts for relevant prospects without automating actions unless an approved integration is configured.', '# Instagram Outreach\n\n## Overview\n\nPrepares Instagram DMs for cases where Instagram is actually relevant. No automation by default.\n\n## Procedure\n\n1. Verify the account is professional/relevant.\n2. Use a visible content signal.\n3. Draft a short human DM.\n4. Route to manual review.\n\n## Verification Checklist\n\n- [ ] Account/source is public and relevant.\n- [ ] DM references a real content signal.\n- [ ] No automated sending.\n', ['sales','instagram','ai-sales']),
}
for name,(desc,body,tags) in secondary.items():
    p = SK / name / 'SKILL.md'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(skill(name, desc, body, tags), encoding='utf-8')

print(json.dumps({
    'crm_accounts': len(accounts),
    'review_items': len(review_files),
    'content_audits': 3,
    'secondary_skills_created': len(secondary),
    'report': str(reports/'2026-07-12-wella-pipeline-report.md'),
    'digest': str(reports/'2026-07-12-daily-orchestration-digest.md')
}, indent=2, ensure_ascii=False))
