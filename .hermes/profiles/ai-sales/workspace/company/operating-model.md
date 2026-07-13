# AI Sales Company — Operating Model

## Principe

Chaque société partenaire traverse la même chaîne. Les équipes ne travaillent pas en silo : elles se passent un dossier enrichi, jamais une consigne vague.

```text
Partner brief
  → ICP Builder
  → Prospect Discovery
  → Signal Detection / Pain Mapping
  → Lead Enrichment
  → Lead Scoring
  → CRM Sync
  → Message Personalization
  → Human Review
  → Outreach sequence draft
  → Reply Triage
  → Meeting Scheduler
  → Handoff Brief
  → Pipeline Report
  → Daily Orchestration
```

## Cas de démonstration actuel

Partenaire : Wella Professionals France / Wella Studio.

Hypothèse commerciale : identifier des salons de coiffure premium, coloristes, studios capillaires et groupes de salons français susceptibles d'être intéressés par les gammes professionnelles Wella, notamment coloration, soin et styling.

## Règles de fonctionnement

1. Frontière de preuve : aucune donnée prospect inventée.
2. Personnalisation : chaque message doit reposer sur un signal réel.
3. Humain dans la boucle : aucun cold outreach automatique au démarrage.
4. CRM d'abord : toute action sérieuse doit laisser une trace.
5. Qualité > volume : exclure les prospects faibles au lieu de remplir artificiellement la liste.

## États de pipeline

- `candidate` : repéré mais non qualifié.
- `qualified` : ICP-fit + signal utile.
- `enriched` : données contact enrichies ou statut `not_found` documenté.
- `scored` : fit × intention × timing évalué.
- `drafted` : message préparé.
- `manual_review` : attend validation humaine.
- `approved` : validé pour envoi.
- `sent` : envoyé via canal autorisé.
- `replied_positive` : réponse positive.
- `replied_objection` : objection à traiter.
- `later` : à relancer plus tard.
- `opt_out` : arrêt définitif.
- `meeting_scheduled` : RDV planifié.
- `discarded` : mauvais fit, preuve insuffisante ou risque.

## Définition d'un run réussi

Un run est réussi s'il produit :

- des fichiers JSON/CSV/Markdown traçables ;
- un CRM local à jour ;
- des messages en review queue ;
- un rapport pipeline ;
- une trace claire des décisions et des limites.
