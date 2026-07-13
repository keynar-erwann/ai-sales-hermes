# Phase 2: Voix & Engagement - Plan d'implémentation

> **Pour Hermes:** Utilisez le skill `subagent-driven-development` pour exécuter ce plan tâche par tâche.

**Objectif :** Créer les capacités d'outreach hyper-personnalisé et multi-canal (email) pour le profil `ai-sales`, avec validation humaine intégrée.

---

### Task 1: Créer le skill `message-personalization`
**Objectif :** Définir la procédure de rédaction pour ancrer chaque outreach sur un signal réel.

**Actions :**
- Créer `/root/.hermes/profiles/ai-sales/skills/ai-sales/message-personalization/SKILL.md`.
- Inclure : doctrine de personnalisation (ancrage signal + valeur), checklist de qualité, et template de réflexion.

### Task 2: Créer le skill `email-sequencing`
**Objectif :** Automatiser la séquence multi-touch par email.

**Actions :**
- Créer `/root/.hermes/profiles/ai-sales/skills/ai-sales/email-sequencing/SKILL.md`.
- Inclure : cadences (J+0, J+3, J+7), gestion de threading, et intégration avec le CRM.

### Task 3: Workflow de validation Slack
**Objectif :** Garantir que chaque message sortant est validé manuellement.

**Actions :**
- Mettre à jour le workflow d'orchestration pour qu'il dépose les brouillons dans `/root/.hermes/profiles/ai-sales/workspace/review-queue/pending`.
- Créer un script simple qui pousse un aperçu du brouillon dans Slack avec les boutons d'action (Valider/Refuser).

---

**Validation :**
- Chaque skill devra avoir son `SKILL.md` avec des étapes claires (frontière de preuve).
- La démo sera validée en rédigeant un email réel pour l'un des prospects en attente dans la `review-queue`.

---
