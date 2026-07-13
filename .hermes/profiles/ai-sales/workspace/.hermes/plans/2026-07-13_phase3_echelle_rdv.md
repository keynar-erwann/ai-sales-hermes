# Phase 3: Échelle & RDV - Plan d'implémentation

> **Pour Hermes:** Utilisez le skill `subagent-driven-development` pour exécuter ce plan tâche par tâche.

**Objectif :** Automatiser la prise de RDV, la gestion des no-shows et le digest quotidien du pipeline à l'échelle pour le profil `ai-sales`.

---

### Task 1: Créer le skill `meeting-scheduler`
**Objectif :** Gérer les créneaux et les invitations.
- **Actions :**
    - Créer `/root/.hermes/profiles/ai-sales/skills/sales/meeting-scheduler/SKILL.md`.
    - Définir la procédure de lecture/écriture du calendrier via MCP (Google Cal).
    - Ajouter les règles de buffers et de gestion de conflits.

### Task 2: Créer le skill `followup-cadence`
**Objectif :** Automatiser les relances post-RDV et la gestion des "no-shows".
- **Actions :**
    - Créer `/root/.hermes/profiles/ai-sales/skills/sales/followup-cadence/SKILL.md`.
    - Définir la logique : rappel 1h avant, relance 15 min après si no-show, envoi du brief de passation avant RDV.

### Task 3: Finaliser `pipeline-report` (Dashboard Slack)
**Objectif :** Pousser le digest quotidien complet.
- **Actions :**
    - Créer `/root/.hermes/profiles/ai-sales/skills/sales/pipeline-report/SKILL.md`.
    - Brancher le script `run_daily.py` (déjà existant) pour qu'il agrège les données CRM et les envoie via la Gateway.

---

**Validation :**
- Vérification de la chaîne complète : Prospect -> Outreach -> RDV -> CRM -> Digest Slack.
- Une fois cette phase terminée, nous passerons au **"Run Complet"** (Show) pour vérifier l'intégrité du produit.
