---
name: email-sequencing
title: Email Sequencing
description: "Orchestre des séquences email multi-touch pour l'outreach B2B."
version: 1.0.0
author: AI Sales Company
license: MIT
metadata:
  hermes:
    tags: [Sales, Outreach, Email, B2B, Sequencing]
    category: sales
    related_skills: [message-personalization, crm-sync, reply-triage]
    requires_toolsets: [gmail, file]
---

# Email Sequencing

Ce skill définit la cadence et la structure des séquences email pour un outreach multi-touch performant et humain.

## Principes de cadence
- **J+0 (Initial)** : Outreach hyper-personnalisé (voir skill `message-personalization`).
- **J+3 (Follow-up 1)** : Apporte une valeur supplémentaire (ressource, étude, audit). Très court.
- **J+7 (Follow-up 2)** : "Dernière tentative" ou question ouverte sur la pertinence du timing.
- **Délai** : Toujours vérifier si une réponse a été reçue avant d'envoyer l'étape suivante (sync avec `reply-triage` et `crm-sync`).

## Processus
1. **Initialisation** : Le chef d'orchestre déclenche la séquence suite à la validation humaine du premier message.
2. **Scheduling** : Chaque étape est planifiée dans le calendrier CRM (`opportunities.json`).
3. **Exécution** : 
   - Avant envoi, vérifier l'état du prospect (Opt-out ? Réponse reçue ?).
   - Utiliser le MCP Gmail pour l'envoi 1:1.
   - Enregistrer l'interaction dans `interactions.json`.

## Structure d'une Séquence
- **Email 1** : Personnalisation profonde (Signal + Valeur).
- **Email 2** : "Bump" contextuel (ex: "Je me demandais si ce sujet était encore d'actualité pour vous ?").
- **Email 3** : "Break-up" (ex: "Je ne veux pas insister si ce n'est pas le moment, je vous laisse la main pour revenir vers moi quand vous serez prêt").

## Mode Sandbox (Mailtrap)
Pour sécuriser la production et éviter les envois accidentels :
1. Configurer Mailtrap (ou un sink SMTP similaire) pour tester le rendu des emails.
2. Utiliser la liste blanche (`whitelist.json`) pour restreindre les envois réels.
3. Le mode "Dry Run" (`prod_mode: false`) doit être activé par défaut dans la config.

## Pièges à éviter
- Ne pas envoyer en masse simultanée (respecter les limites Gmail).
- Toujours vérifier le statut `opt_outs.json` avant tout envoi.

## Sandbox / Production Workflow
- **Utilisation de Mailtrap** : Pour tout développement ou test, le skill DOIT pointer vers `sandbox.smtp.mailtrap.io`.
- **Mode Sandbox** : Ne jamais envoyer d'emails réels via un SMTP externe sans avoir testé le flux dans Mailtrap au préalable.
- **Sécurisation** : Les accès SMTP (host, port, user, password) doivent être configurés via `hermes config` et non codés en dur.
- **Workflow d'Approvisionnement** : Utiliser `slack_bot.py` pour valider les drafts, et `smtp_sender.py` pour envoyer via la configuration sécurisée de Hermes.
