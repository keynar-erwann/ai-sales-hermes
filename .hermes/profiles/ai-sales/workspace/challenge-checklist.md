# Challenge Checklist — AI Sales Company dans Hermes

Source du brief copié dans ce workspace :

```text
/root/.hermes/profiles/ai-sales/workspace/CHALLENGE.md
```

Profil : `ai-sales`

Partenaire de démonstration choisi : Wella Professionals France / Wella Studio

Brief partenaire :

```text
/root/.hermes/profiles/ai-sales/workspace/partner-brief-wella-professionals-fr.md
```

## Objectif exact du challenge

Construire dans Hermes une société commerciale IA coordonnée qui, pour une société partenaire donnée, couvre le cycle B2B de bout en bout :

1. trouver les bons prospects ;
2. analyser leurs signaux et points de tension ;
3. engager avec des messages hyper-personnalisés ;
4. gérer les rendez-vous ;
5. produire du contenu à valeur ;
6. maintenir un CRM propre ;
7. orchestrer une boucle quotidienne ;
8. documenter les skills et montrer une démo end-to-end.

## Barème du challenge

| Critère | Points | Statut actuel |
|---|---:|---|
| Qualité de la personnalisation | 25 | À construire |
| Orchestration multi-équipes | 20 | Operating model 5 équipes créé, boucle à démontrer |
| Design des skills | 15 | 8 skills faits, skills secondaires manquants |
| Intégrité CRM + frontière de preuve | 15 | CRM local initialisé, sync à démontrer |
| Démo end-to-end | 15 | Cas Wella choisi, run à produire |
| Créativité + vision 360° | 10 | À renforcer via audits/offres/digest |

## Architecture cible demandée

```text
Partner brief
  → ICP Builder
  → Prospect Discovery
  → Signal Detection
  → Pain Mapping
  → Lead Enrichment
  → Lead Scoring
  → CRM Sync
  → Message Personalization
  → Human Review / Slack
  → Email / LinkedIn / Instagram sequence
  → Reply Triage
  → Meeting Scheduler
  → Handoff Brief
  → Pipeline Report
  → Daily Orchestration
```

## État actuel réel

### Fait

- [x] Profil Hermes `ai-sales` créé.
- [x] Doctrine renforcée dans `SOUL.md`.
- [x] Workspace structuré.
- [x] README d'architecture créé.
- [x] Hunter.io intégré via `lead-enrichment`.
- [x] Script Hunter.io créé : `hunter_client.py`.
- [x] Skill `lead-enrichment` créé.
- [x] Skill `prospect-discovery` créé.
- [x] Partenaire de démo choisi : Wella Professionals France.
- [x] Brief partenaire Wella créé.
- [x] `CHALLENGE.md` copié dans le workspace `ai-sales`.
- [x] Operating System 5 équipes créé dans `workspace/company/`.
- [x] Dossiers d'équipes créés dans `workspace/team-*`.
- [x] CRM local initialisé dans `workspace/crm/`.
- [x] Skill `icp-builder` créé.
- [x] Skill `lead-scoring` créé.
- [x] Skill `crm-sync` créé.
- [x] Skill `message-personalization` créé.
- [x] Skill `pipeline-report` créé.
- [x] Skill `daily-orchestration` créé.

### Partiellement fait

- [x] ICP Wella : skill `icp-builder` créé et livrable `icp.md` produit.
- [x] Prospection : run Wella produit avec 20 leads et 40 candidats sauvegardés.
- [x] Enrichissement : Hunter.io volontairement non appliqué car aucun décideur nommé fiable ; statut `not_found` documenté.
- [x] Frontière de preuve matérialisée dans `sources.md`, `discovery.json`, CRM et review queue.
- [x] Orchestration : workflow, skill et digest Wella créés.

### Manquant

- [x] CRM local initialisé.
- [x] Skill `icp-builder`.
- [x] Skill `signal-detection`.
- [x] Skill `pain-mapping`.
- [x] Skill `lead-scoring`.
- [x] Skill `message-personalization`.
- [x] Skill `email-sequencing`.
- [x] Skill `reply-triage`.
- [x] Skill `objection-handling`.
- [x] Skill `meeting-scheduler`.
- [x] Skill `followup-cadence`.
- [x] Skill `handoff-brief`.
- [x] Skill `marketing-audit`.
- [x] Skill `personalized-offer`.
- [x] Skill `crm-sync`.
- [x] Skill `daily-orchestration`.
- [x] Skill `pipeline-report`.
- [ ] Slack validation humaine réelle non branchée ; review queue locale créée comme MVP.
- [ ] Gmail / Resend réel non branché ; `email-sequencing` et drafts locaux créés.
- [x] LinkedIn / Instagram skills créés en mode préparation sûre, sans automatisation.
- [x] Démo finale A→Z local-first créée pour Wella.
- [x] Runbook démo créé dans `workspace/demo/runbook.md`.
- [x] Transcript de run créé dans `workspace/demo/transcript.md` ; capture/vidéo réelle encore optionnelle.
- [ ] Repo GitHub sous `keynar-erwann`.

## Jalons du brief

### S1 — SOCLE

Brief : fondations + prospection. Profil Hermes `ai-sales`, `SOUL.md`, ICP, skill de découverte → 20 leads enrichis avec leurs signaux.

Statut : en cours, proche mais pas terminé.

Fait :

- [x] Profil `ai-sales`.
- [x] `SOUL.md`.
- [x] Skill `prospect-discovery`.
- [x] Skill `lead-enrichment`.
- [x] Hunter.io.
- [x] Brief Wella.

À faire :

- [x] Créer un livrable ICP Wella.
- [x] Créer le run Wella.
- [x] Trouver 30-40 salons candidats.
- [x] Sélectionner 20 leads qualifiés.
- [x] Pour chaque lead : entreprise, site, ville, rôle cible non nommé, signal, source, pain hypothesis, score, next action.
- [x] Enrichissement Hunter.io évalué : non exécuté car personne nommée fiable absente ; aucun email deviné.
- [x] Exporter JSON + CSV + sources.

Livrables S1 :

```text
workspace/prospect-runs/2026-07-12-wella-professionals-fr/README.md
workspace/prospect-runs/2026-07-12-wella-professionals-fr/icp.md
workspace/prospect-runs/2026-07-12-wella-professionals-fr/discovery.json
workspace/prospect-runs/2026-07-12-wella-professionals-fr/discovery.csv
workspace/prospect-runs/2026-07-12-wella-professionals-fr/sources.md
```

### S2 — VOIX

Brief : personnalisation + 1 canal. Skills de personnalisation + séquence email, sync CRM. Premiers messages validés en Slack.

Statut : MVP local-first terminé ; Slack réel non branché.

À faire :

- [x] Créer `message-personalization`.
- [x] Créer `email-sequencing`.
- [x] Créer `crm-sync` minimal.
- [x] Créer une review queue humaine.
- [x] Produire une simulation locale claire de validation humaine via review queue.
- [x] Générer les premiers messages Wella pour 5 leads.
- [x] Marquer tous les messages en `manual_review`.

Livrables S2 :

```text
skills/ai-sales/message-personalization/SKILL.md
skills/ai-sales/email-sequencing/SKILL.md
skills/ai-sales/crm-sync/SKILL.md
workspace/crm/accounts.json
workspace/crm/contacts.json
workspace/crm/interactions.json
workspace/review-queue/pending/*.md
```

### S3 — ÉCHELLE

Brief : multi-canal + RDV. LinkedIn/Instagram, scheduling, relances, digest Slack quotidien.

Statut : version sûre local-first terminée ; intégrations plateforme réelles à brancher ensuite.

À faire :

- [x] Définir une stratégie LinkedIn/Instagram conforme ToS : préparation uniquement, pas d'automatisation sans intégration approuvée.
- [x] Créer ou documenter `linkedin-outreach` en mode préparation / non-envoi si intégration absente.
- [x] Créer ou documenter `instagram-outreach` en mode préparation / non-envoi si intégration absente.
- [x] Créer `meeting-scheduler`.
- [x] Créer `followup-cadence`.
- [x] Créer `reply-triage`.
- [x] Créer `pipeline-report` avec digest quotidien.
- [x] Prévoir alternative locale démontrable via reports/digest.

Livrables S3 :

```text
skills/ai-sales/reply-triage/SKILL.md
skills/ai-sales/followup-cadence/SKILL.md
skills/ai-sales/meeting-scheduler/SKILL.md
skills/ai-sales/pipeline-report/SKILL.md
workspace/reports/2026-07-12-daily-orchestration-digest.md
```

### S4 — SHOW

Brief : orchestration + démo. La boucle complète qui tourne sur une vraie société partenaire, + documentation des skills.

Statut : démo local-first Wella créée ; repo GitHub/capture vidéo restent à faire.

À faire :

- [x] Créer `daily-orchestration`.
- [x] Écrire le script et la procédure de démo end-to-end.
- [x] Faire tourner la boucle complète local-first sur Wella.
- [x] Produire le rapport final.
- [x] Préparer le runbook final.
- [x] Préparer transcript de run.
- [ ] Préparer repo GitHub.

Livrables S4 :

```text
skills/ai-sales/daily-orchestration/SKILL.md
workspace/reports/final-demo-wella.md
workspace/demo/runbook.md
workspace/demo/transcript.md
workspace/demo/runbook.md + workspace/README.md
```

## Plan d'exécution recommandé

### Phase 1 — Verrouiller S1 Wella

1. Créer `icp-builder` ou au minimum `icp.md` pour Wella.
2. Lancer la découverte Wella.
3. Produire 20 leads avec sources.
4. Appliquer Hunter.io seulement aux meilleurs leads avec domaine + personne fiable.
5. Sauvegarder JSON/CSV/sources.

### Phase 2 — Construire le cœur produit

1. Créer CRM local.
2. Créer `crm-sync`.
3. Importer les 20 leads Wella dans CRM.
4. Créer `message-personalization`.
5. Générer messages personnalisés pour les meilleurs leads.
6. Créer review queue humaine.

### Phase 3 — Montrer l'orchestration

1. Créer `pipeline-report`.
2. Créer `daily-orchestration`.
3. Créer `reply-triage` et `followup-cadence` en version démontrable.
4. Produire un digest quotidien local ou Slack si configuré.

### Phase 4 — Ajouter les éléments différenciants

1. Créer `marketing-audit`.
2. Créer `personalized-offer`.
3. Générer 2-3 mini-audits Wella pour les meilleurs salons.
4. Ajouter un handoff brief de RDV.

### Phase 5 — Packaging final

1. Nettoyer les skills.
2. Écrire README final.
3. Documenter la démo.
4. Créer un transcript/capture.
5. Préparer le repo GitHub.

## Priorité immédiate

Ne pas partir directement sur toutes les intégrations.

Prochaine action recommandée : finir S1 proprement sur Wella, parce que tous les autres blocs dépendent d'une base de leads réelle et sourcée.

Ordre immédiat :

1. `icp.md` Wella.
2. Run Wella 20 leads.
3. CRM local.
4. `message-personalization`.
5. Review queue.
6. Pipeline report.
7. Daily orchestration.

## Garde-fous non négociables

- Aucun lead inventé.
- Aucun décideur inventé.
- Aucun email deviné.
- Aucun outreach automatique avant validation humaine.
- Chaque message doit citer implicitement un signal réel.
- Chaque statut doit être traçable.
- Un prospect faible doit être exclu plutôt que gonfler artificiellement le volume.


## Mise à niveau configuration — 2026-07-14

- [x] `CHALLENGE.md` lu et copié dans le workspace.
- [x] `SOUL.md` réaligné sur la mission complète, pas seulement S1.
- [x] 20 skills cibles présents sous `skills/ai-sales/`.
- [x] Workspace 5 équipes, CRM, review queue, reports présents.
- [x] Scripts corrigés : plus de credentials hardcodés, lecture `.env`, fail-safe human-in-the-loop.
- [x] Mailtrap SMTP vérifié en login avec les credentials du profil.
- [x] Slack Bot token vérifié et canal `ai-sales` détecté (`SLACK_HOME_CHANNEL`).
- [ ] Slack Socket Mode entrant : `SLACK_APP_TOKEN` actuel refusé par Slack (`invalid_auth`). À corriger côté Slack App avec un app-level token `xapp-...` scope `connections:write`, puis redémarrer `hermes -p ai-sales gateway restart`.
- [x] Cron/daily loop documenté : digest et notifications Slack, envoi uniquement des drafts approuvés.
