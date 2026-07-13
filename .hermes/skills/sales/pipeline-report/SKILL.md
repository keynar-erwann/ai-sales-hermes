---
name: pipeline-report
title: Pipeline Report
description: "Génère et envoie le digest quotidien du pipeline CRM vers Slack."
version: 1.0.0
author: AI Sales Company
license: MIT
metadata:
  hermes:
    tags: [Sales, CRM, Reporting, Slack, Pipeline]
    category: sales
    related_skills: [crm-sync, daily-orchestration]
    requires_toolsets: [file, gateway]
---

# Pipeline Report

Ce skill orchestre la génération et l'envoi du digest quotidien du pipeline commercial.

## Objectif
Donner au manager humain une vision claire, immédiate et actionnable sur la santé du pipeline sans avoir à ouvrir le CRM.

## Processus
1. **Agrégation** : Lire les données du jour dans `/root/.hermes/profiles/ai-sales/workspace/crm/`.
2. **Analyse** :
   - Identifier les nouveaux leads validés.
   - Lister les rendez-vous du jour.
   - Détecter les "at-risk" (prospects sans réponse depuis > 5 jours).
3. **Génération** : Rédiger un rapport structuré (Markdown) :
   - 🚨 **Review Queue** : Liste des brouillons en attente.
   - 📊 **Pipeline Status** : Nombre de leads, RDV pris, opportunités en cours.
   - ⚠️ **Action Items** : Les relances urgentes ou les no-shows à traiter.
4. **Diffusion** : Envoyer le digest via la Gateway Slack (`hermes gateway send`) dans le canal configuré.

## Règles d'or
- **Actionnabilité** : Ne pas donner des chiffres bruts, donner des listes d'actions (ex: "Relancer X").
- **Brièveté** : Moins de 15 lignes de texte.
- **Fiabilité** : Si une donnée CRM est manquante, le rapporter comme "Data Incomplete" au lieu d'halluciner.
