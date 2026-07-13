# Orchestra Agent · AI Sales Company

Ce projet implémente une **société commerciale pilotée par des agents IA autonomes** via l'infrastructure [Hermes Agent](https://hermes-agent.nousresearch.com/). Cette solution automatise le cycle de vente B2B, de la prospection hyper-personnalisée à la gestion des rendez-vous.

## 🚀 Vision

L'objectif est de recréer les fonctions d'une équipe de vente performante : 
- Prospection : Recherche et qualification de leads via signaux réels (levées de fonds, recrutements, presse)
- Outreach : Personnalisation profonde (zéro template générique)
- Validation Humaine : Workflow Slack natif pour valider chaque message avant envoi
- Orchestration : Boucle quotidienne automatisée assurant l'hygiène du pipeline CRM

## 🏗 Architecture (Les 5 Équipes)

Le projet est organisé par délégations spécialisées :
1. Prospection & Intelligence : Analyse les signaux et enrichit les leads
2. Outreach & Engagement : Rédige des approches uniques et gère les objections
3. Admin & Rendez-vous : Planification, gestion de calendrier et brief de passation
4. Content & Marketing : Audit express et offres personnalisées
5. CRM & Orchestration : Pilote la boucle quotidienne et le reporting

## 🛠 Installation & Setup

### 1. Prérequis
- Hermes Agent installé
- Python 3.14+ avec slack_sdk et python-dotenv

### 2. Configuration
- Copiez le fichier `.env.example` en `.env` et renseignez vos credentials (SMTP Mailtrap, Slack Tokens)
- Configurez le profil via Hermes :
  ```bash
  hermes profile create ai-sales
  ```

## 🤖 Workflow Opérationnel

Le système tourne de manière autonome via un orchestrateur central :

1. **Daily Run** : Le cronjob (9h00) scanne les leads et génère les brouillons
2. **Review Queue** : Les drafts sont déposés dans `review-queue/pending/`
3. **Validation Slack** : Recevez les alertes sur Slack. Approuvez avec : `APPROVE <filename>`
4. **Envoi** : Le bot `slack_bot.py` détecte l'approbation et envoie le mail via SMTP (Sandbox)

## 🛡 Sécurité & Doctrine

- Frontière de preuve : Chaque affirmation sur un prospect est sourcée
- Humain-dans-la-boucle : Aucun envoi n'est automatisé sans validation humaine explicite
- RGPD & Respect : Pas de scraping abusif, gestion stricte des opt-outs

## 📁 Structure du projet

```
├── crm/                 # Source de vérité (JSON transactionnel)
├── demo/                # Scripts de découverte de leads
├── outreach-drafts/     # Brouillons personnalisés
├── review-queue/        # Files d'attente (pending/approved)
├── scripts/             # Orchestrateurs (bot, sender, daily)
└── skills/              # Procédures réutilisables (SKILL.md)
```

---

Projet développé pour le Challenge Orchestra Intelligence.