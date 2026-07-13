# Review Queue System

Ce dossier contient les leads en attente de validation humaine avant envoi d'outreach.

## Processus
1. **Agent** : Dépose un fichier `.md` dans `pending/` (format `nom-prospect.md`).
2. **Notification** : Le système prévient l'humain via Slack.
3. **Validation** : L'humain approuve (déplace vers `approved/`) ou refuse (déplace vers `rejected/` ou demande modification).

## Structure
- `/pending/` : En attente.
- `/approved/` : Prêt pour l'envoi.
- `/rejected/` : À retravailler.
