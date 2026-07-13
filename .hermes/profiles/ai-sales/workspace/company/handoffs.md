# AI Sales Company — Handoffs entre équipes

## Format standard d'un dossier lead

```json
{
  "account": {
    "name": "",
    "domain": "",
    "city": "",
    "source_urls": []
  },
  "person": {
    "first_name": "",
    "last_name": "",
    "title": "",
    "linkedin_url": "",
    "source_urls": []
  },
  "signal": {
    "type": "",
    "summary": "",
    "source_url": "",
    "observed_date": ""
  },
  "pain_hypothesis": "",
  "score": {
    "fit": null,
    "intent": null,
    "timing": null,
    "total": null,
    "reason": ""
  },
  "email": {
    "address": "",
    "status": "not_found",
    "hunter_score": null,
    "source_urls": []
  },
  "crm": {
    "stage": "candidate",
    "owner_team": "prospection-intelligence",
    "next_action": "research_more"
  },
  "proof": {
    "checked_at": "",
    "notes": []
  }
}
```

## Handoff 1 — Prospection vers CRM

Condition : compte réel + source + signal ou raison de recherche supplémentaire.

Sortie attendue : record CRM `candidate` ou `qualified`.

## Handoff 2 — CRM vers Outreach

Condition : lead `qualified` ou `scored`, avec signal réel et pain hypothesis.

Sortie attendue : draft en `review-queue/pending`, jamais envoyé automatiquement.

## Handoff 3 — Outreach vers Admin

Condition : réponse positive ou intérêt simulé dans la démo.

Sortie attendue : créneaux proposés + handoff brief.

## Handoff 4 — Content vers Outreach

Condition : lead prioritaire ou compte stratégique.

Sortie attendue : audit express ou one-pager personnalisé qui donne une raison concrète de répondre.

## Handoff 5 — Orchestration quotidienne

Condition : chaque début de run ou demande de reporting.

Sortie attendue : liste d'actions priorisées par équipe, risques, blocages et prochaines décisions.
