---
name: meeting-scheduler
title: Meeting Scheduler
description: "Automatise la gestion des créneaux, les réservations et les invitations."
version: 1.0.0
author: AI Sales Company
license: MIT
metadata:
  hermes:
    tags: [Sales, Scheduling, Calendar, B2B]
    category: sales
    related_skills: [crm-sync, followup-cadence]
    requires_toolsets: [google-workspace, file]
---

# Meeting Scheduler

Ce skill assure une gestion fluide des rendez-vous commerciaux, depuis la proposition de créneaux jusqu'à l'invitation finale.

## Principes de gestion
1. **Disponibilité intelligente** : Utiliser des buffers de 15 min avant/après chaque RDV pour éviter les enchaînements serrés.
2. **Contextualisation** : Chaque invitation doit inclure les liens vers le CRM (`interactions.json`) et le brief de passation.
3. **Réactivité** : Proposer toujours au moins 3 créneaux dans des fuseaux horaires pertinents pour le prospect.

## Processus
1. **Proposition** : Suite à un "oui" du prospect, extraire les disponibilités depuis le calendrier (via MCP Google Cal).
2. **Réservation** : 
   - Bloquer le créneau temporairement si nécessaire.
   - Envoyer l'invitation officielle.
3. **Confirmation** : Mettre à jour le CRM (`opportunities.json`) avec le statut "RDV fixé".
4. **Passation** : Générer le brief de passation pour le commercial interne.

## Pièges à éviter
- Ne jamais envoyer d'invitation sans avoir vérifié les conflits potentiels dans le calendrier.
- Toujours inclure un lien de reschedule/annulation dans le corps de l'invitation.
