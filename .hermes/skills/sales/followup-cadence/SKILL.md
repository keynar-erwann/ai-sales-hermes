---
name: followup-cadence
title: Follow-up Cadence
description: "Gère les relances, rappels de RDV et no-shows."
version: 1.0.0
author: AI Sales Company
license: MIT
metadata:
  hermes:
    tags: [Sales, Follow-up, Meetings, B2B]
    category: sales
    related_skills: [meeting-scheduler, crm-sync]
    requires_toolsets: [gmail, file]
---

# Follow-up Cadence

Ce skill gère la communication entourant le rendez-vous commercial pour maximiser les taux de présence et assurer une passation efficace.

## Processus de suivi
1. **Rappel pré-RDV (H-1h)** : 
   - Envoyer un rappel amical avec le lien de visioconférence.
   - Joindre un résumé rapide de l'ordre du jour.
2. **Gestion des No-shows** :
   - Si le prospect est absent à l'heure du RDV (attendre 10-15 min), envoyer un mail "Je crois que nous nous sommes manqués".
   - Proposer de reprogrammer.
3. **Passation (Post-RDV)** :
   - Si le RDV a eu lieu, envoyer un email de remerciement avec le compte-rendu.
   - Mettre à jour le statut dans le CRM (`opportunities.json`).

## Règles d'or
- **Ne jamais blâmer** : Toujours laisser une porte de sortie au prospect (ex: "J'imagine que vous avez eu une urgence").
- **Automatisation vs Humain** : Les no-shows critiques sont remontés dans la `review-queue` pour une décision humaine avant relance agressive.

## Pièges à éviter
- Envoyer des relances si le prospect a déjà annulé ou reprogrammé.
- Oublier de mettre à jour le CRM après chaque interaction.
