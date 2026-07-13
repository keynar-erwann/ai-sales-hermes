# AI Sales Company — Hermes Profile

Profil Hermes : `ai-sales`

Objectif : recréer dans Hermes une société commerciale IA capable de prospecter, enrichir, personnaliser, suivre et orchestrer un pipeline B2B pour une société partenaire.

Ce profil suit le brief `CHALLENGE.md` : qualité de personnalisation, orchestration multi-équipes, skills robustes, frontière de preuve, CRM, et démo end-to-end.

## Architecture

```text
Partner brief
  → ICP Builder
  → Prospect Discovery
  → Lead Enrichment / Hunter.io
  → Lead Scoring
  → CRM / Source of Truth
  → Message Personalization
  → Human Review
  → Outreach
  → Reply Triage
  → Meeting Scheduling
  → Pipeline Reporting
```

## Équipes cibles

### 1. Prospection & Intelligence

Responsabilité : trouver qui contacter et pourquoi maintenant.

Skills actuels :

- `prospect-discovery`
- `lead-enrichment`
- `icp-builder`
- `lead-scoring`

Statut : première brique opérationnelle.

### 2. Outreach & Engagement

Responsabilité : rédiger et gérer l'engagement multicanal.

Skills à construire :

- `message-personalization` ✅ créé en MVP local-first
- `email-sequencing`
- `reply-triage`
- `objection-handling`

Statut : à faire après la première démo de leads.

### 3. Admin & Rendez-vous

Responsabilité : transformer un oui en rendez-vous tenu.

Skills à construire :

- `meeting-scheduler`
- `followup-cadence`
- `handoff-brief`

### 4. Content & Marketing

Responsabilité : créer de la valeur avant la demande.

Skills à construire :

- `marketing-audit`
- `personalized-offer`

### 5. CRM & Orchestration

Responsabilité : source de vérité, boucle quotidienne, reporting.

Skills à construire :

- `crm-sync` ✅ créé en MVP local-first
- `daily-orchestration` ✅ créé en MVP local-first
- `pipeline-report` ✅ créé en MVP local-first

## Operating System 5 équipes

Documentation créée :

```text
/root/.hermes/profiles/ai-sales/workspace/company/teams.md
/root/.hermes/profiles/ai-sales/workspace/company/operating-model.md
/root/.hermes/profiles/ai-sales/workspace/company/handoffs.md
```

Dossiers d'équipe :

```text
/root/.hermes/profiles/ai-sales/workspace/team-1-prospection-intelligence/
/root/.hermes/profiles/ai-sales/workspace/team-2-outreach-engagement/
/root/.hermes/profiles/ai-sales/workspace/team-3-admin-rdv/
/root/.hermes/profiles/ai-sales/workspace/team-4-content-marketing/
/root/.hermes/profiles/ai-sales/workspace/team-5-crm-orchestration/
```

## Skills installés pour ai-sales

### `lead-enrichment`

Chemin :

```text
/root/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/SKILL.md
```

Script Hunter.io :

```text
/root/.hermes/profiles/ai-sales/skills/ai-sales/lead-enrichment/scripts/hunter_client.py
```

Commandes :

```bash
python3 hunter_client.py account
python3 hunter_client.py domain-search --domain stripe.com --limit 3
python3 hunter_client.py email-finder --domain stripe.com --first-name Kevin --last-name Bognar
python3 hunter_client.py email-verifier --email kbognar@stripe.com
python3 hunter_client.py lead-record --company Stripe --domain stripe.com --first-name Kevin --last-name Bognar
```

Règles :

- ne jamais deviner un email ;
- vérifier avant usage ;
- conserver les sources Hunter.io ;
- sortir `manual_review` avant tout outreach.

### `prospect-discovery`

Chemin :

```text
/root/.hermes/profiles/ai-sales/skills/ai-sales/prospect-discovery/SKILL.md
```

Rôle : découvrir les comptes ICP-fit, décideurs et signaux récents, puis passer les meilleurs candidats à `lead-enrichment`.

Template de run :

```text
/root/.hermes/profiles/ai-sales/skills/ai-sales/prospect-discovery/templates/run-readme.md
```

## Variables d'environnement

Fichier :

```text
/root/.hermes/profiles/ai-sales/.env
```

Actuellement requis pour Hunter.io :

```bash
HUNTER_API_KEY=...
```

Ne jamais committer ou afficher les secrets.

## Dossiers de travail recommandés

```text
/root/.hermes/profiles/ai-sales/workspace/prospect-runs/
/root/.hermes/profiles/ai-sales/workspace/crm/
/root/.hermes/profiles/ai-sales/workspace/review-queue/
/root/.hermes/profiles/ai-sales/workspace/reports/
```

## Format d'un run de prospection

```text
workspace/prospect-runs/YYYY-MM-DD-partner-slug/
  README.md
  discovery.json
  discovery.csv
  sources.md
```

Chaque lead doit contenir :

- company name + domain ;
- decision-maker + title ;
- proof URL for company/person ;
- recent trigger signal + source URL ;
- pain hypothesis ;
- score ;
- Hunter.io email status ;
- next action.

## Commande de démo S1

Dans une nouvelle session `ai-sales` :

```text
Utilise prospect-discovery pour trouver 20 leads pour une agence IA qui vend des agents commerciaux IA aux startups B2B SaaS françaises. Pour chaque lead : entreprise, décideur, rôle, signal récent, source, pain hypothesis, score, statut email Hunter.io si disponible, next_action. Sauvegarde les résultats dans workspace/prospect-runs/.
```

## Règles qualité

- Zéro donnée inventée.
- Un signal réel par lead.
- Un email non vérifié ne sert pas à envoyer.
- Pas d'outreach sans validation humaine.
- Les prospects faibles sont exclus au lieu d'être ajoutés pour faire du volume.

## Roadmap immédiate

1. Produire une première démo 20 leads.
2. Ajouter un CRM minimal : CSV/JSON local d'abord, puis Airtable/HubSpot/Attio.
3. Créer `message-personalization`.
4. Créer une review queue humaine.
5. Brancher Slack pour validation/digest.
