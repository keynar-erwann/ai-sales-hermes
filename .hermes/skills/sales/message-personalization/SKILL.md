---
name: message-personalization
title: Message Personalization
description: "Rédige des messages d'outreach hyper-personnalisés ancrés sur des signaux réels."
version: 1.0.0
author: AI Sales Company
license: MIT
metadata:
  hermes:
    tags: [Sales, Outreach, Personalization, B2B]
    category: sales
    related_skills: [lead-enrichment, reply-triage, objection-handling]
    requires_toolsets: [web, terminal, file]
---

# Message Personalization

L'objectif est de produire un outreach indiscernable d'un commercial humain. Chaque message doit être ancré sur un signal réel et récent trouvé par l'équipe de prospection.

## Principes clés
1. **Signal-First** : Aucun message ne commence sans un signal récent (levée, recrutement, news).
2. **Valeur ajoutée** : Le message apporte un insight ou une observation utile avant la demande d'appel.
3. **Zéro template générique** : Chaque structure est réadaptée au contexte du prospect.
4. **Validation obligatoire** : Tout message préparé par l'IA doit être validé via la `review-queue` avant envoi.

## Workflow "Prod-Ready" (Intégration Slack/Mailtrap)
- **Sandbox** : Utiliser Mailtrap (SMTP sandbox) pour tous les tests d'envoi.
- **Sécurité** : Ne jamais stocker de secrets (clés API) en dur dans les scripts. Utiliser un fichier `.env` chargé par `python-dotenv`.
- **Automatisation** : Utiliser un bot (`slack_bot.py`) pour surveiller les instructions Slack et déclencher les envois via `orchestra_sender.py`.

## Workflow de Validation Slack
- Le script `scripts/review_manager.py` utilise un webhook Slack (configuré dans `config.yaml` via `gateway.slack.webhook_url`).
- Chaque nouveau brouillon dans `pending/` est envoyé automatiquement sur Slack via ce script.
- La validation humaine est requise : une fois le message reçu sur Slack, la confirmation humaine permet de basculer le fichier vers `approved/`.

## Structure du Draft
```markdown
# [Nom du prospect] - Personalization Draft

## Signal utilisé
- [Description du signal + URL de source]

## Draft
Objet : [Objet personnalisé]

[Texte du message]

## Prochaine étape
- [Action prévue après validation]
```
