---
name: daily-orchestration
title: Daily Orchestration
description: "Boucle quotidienne de pilotage : lecture du pipeline, délégation aux équipes, reporting."
version: 1.0.0
author: AI Sales Company
license: MIT
metadata:
  hermes:
    tags: [Orchestration, Pipeline, CRM, Management]
    category: sales
    related_skills: [crm-sync, pipeline-report, reply-triage]
    requires_toolsets: [terminal, file]
---

# Daily Orchestration

Le skill "Chef d'Orchestre". Chaque matin (ou déclenchement), il examine l'état des leads dans le CRM et la Review Queue pour décider des prochaines actions.

## Boucle quotidienne
1. **Sync CRM** : Lecture de `/crm/opportunities.json`.
2. **Review Queue Check** : Quels leads sont en attente de validation (`pending/`) ?
3. **Réponses entrantes** : Lecture des nouvelles interactions via `reply-triage`.
4. **Action** : 
   - Si un lead est en `pending` : envoyer une alerte Slack pour validation humaine.
   - Si un lead a une réponse : déléguer au skill `objection-handling` ou `meeting-scheduler`.
   - Si un lead est inactif depuis trop longtemps : marquer pour relance.
5. **Digest** : Générer le rapport quotidien pour Slack (`pipeline-report`).

## Rôle
Déléguer les tâches aux équipes spécialisées. Le chef d'orchestre ne rédige pas les emails lui-même, il dit à l'équipe "Outreach & Engagement" ou "Admin & RDV" de le faire.
