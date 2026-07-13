---
name: prospect-discovery
title: Prospect Discovery
description: "Find target accounts and key decision makers using web research and public data."
version: 1.0.0
author: Orchestra AI Sales Team
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Sales, Prospecting, Lead Generation, B2B, Account Discovery]
    category: sales
    related_skills: [icp-builder, signal-detection, lead-enrichment]
    requires_toolsets: [web, terminal, file]
---

# Prospect Discovery

Trouve les comptes cibles et les décideurs clés en utilisant des recherches web et des données publiques, en respectant l'ICP (Ideal Customer Profile).

## When to Use This Skill

Use this skill when:
- Tu dois identifier des comptes cibles pour une société partenaire
- Tu dois trouver les décideurs clés (CEO, CTO, Head of Sales, etc.) dans ces comptes
- Tu dois collecter des informations de base sur les comptes (secteur, taille, localisation, site web)

## When NOT to Use This Skill

- Pour de l'enrichissement détaillé des leads → use `lead-enrichment` skill
- Pour la détection de trigger events → use `signal-detection` skill
- Pour la définition de l'ICP → use `icp-builder` skill

## Core Principles

1. **Frontière de preuve** : Toutes les informations collectées doivent être sourcées (URL des pages web consultées)
2. **Respect RGPD** : Aucun scraping abusif, uniquement des données publiques
3. **Priorité à la qualité** : Mieux 5 leads qualifiés que 50 leads génériques

## Step 1: Understand the Target ICP

Before starting, ensure you have a clear ICP (Ideal Customer Profile) for the partner company:
- Secteur d'activité
- Taille de l'entreprise (CA, nombre d'employés)
- Localisation géographique
- Technologies utilisées (si applicable)
- Postes des décideurs ciblés

If no ICP exists yet, use the `icp-builder` skill first.

## Step 2: Find Target Accounts

Use web searches to identify companies matching the ICP:
```
Queries examples (in French or English based on target region):
- "[Secteur] companies [Taille] in [Région]"
- "Top [X] [Secteur] startups in [Pays]"
- "Companies using [Technologie] in [Région]"
```

For each company, collect:
- Nom de l'entreprise
- Site web
- Secteur d'activité
- Taille (nombre d'employés, CA si disponible)
- Localisation (ville, pays)
- URL de la page "À propos" ou "Team"
- URL du LinkedIn de l'entreprise

### Tools to Use
- `web_search` : pour trouver des listes d'entreprises
- `web_extract` : pour extraire les informations des sites web

## Step 3: Identify Key Decision Makers

For each target account, find the key decision makers:
- C-level (CEO, CTO, CFO, CMO)
- Heads of Department (Head of Sales, Head of Marketing, Head of Engineering)
- Founders (for startups)

Collect for each decision maker:
- Nom complet
- Poste
- LinkedIn profile URL
- Email professionnel (si disponible publiquement)

### How to Find Decision Makers
1. Visit the company's "Team" or "About Us" page
2. Search LinkedIn: `[Nom de l'entreprise] [Poste]`
3. Check press releases or news articles about the company

### Tools to Use
- `web_extract` : pour extraire les informations des pages "Team"
- `web_search` : pour trouver les profils LinkedIn

## Step 4: Document Everything

For each discovered prospect, document all information with sources in a structured format (Markdown table or JSON file).

Example Markdown format:
```markdown
# Prospects Découverts

## Compte: [Nom de l'entreprise]
- Site web: [URL]
- Secteur: [Secteur]
- Taille: [Nombre d'employés]
- Localisation: [Ville, Pays]
- Sources: [URLs]

### Décideurs:
| Nom | Poste | LinkedIn | Email | Source |
|-----|-------|----------|-------|--------|
| [Nom] | [Poste] | [URL] | [Email si disponible] | [URL] |
```

## Step 5: Validate & Prioritize

Quickly validate that each prospect matches the ICP, and prioritize based on:
- Fit avec l'ICP
- Signaux d'intention (si déjà disponibles)
- Taille de l'entreprise

## Limitations

- Ne collecte que des données publiques (pas de données privées ou payantes)
- Ne vérifie pas les emails (utilisez `lead-enrichment` pour ça)
- Ne détecte pas les trigger events (utilisez `signal-detection` pour ça)