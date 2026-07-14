# Generic Company Demo — AI Sales Company

Objectif : démontrer que `ai-sales` n’est pas codé pour Wella. Wella est le cas pré-préparé et rapide. Pour une autre société partenaire, le profil doit repartir d’un brief partenaire et produire un nouveau run sourcé.

## Positionnement à dire pendant la démo

"Wella est mon scénario de démonstration préparé pour éviter les temps morts. Mais l’agent n’est pas un workflow Wella : il lit un brief partenaire, construit l’ICP, cherche les prospects, documente les sources, synchronise le CRM, prépare les messages et passe par validation humaine. On peut lui donner une autre boîte et il relance le même operating model."

## Prompt Slack pour une autre entreprise

À envoyer dans `#ai-sales` :

```text
@Hermes Orchestra, nouvelle démo avec une autre société partenaire.

Société partenaire : <NOM DE LA BOÎTE>
Site : <URL si connue>
Offre à vendre : <CE QU’ELLE VEND>
Marché cible : <PAYS / SEGMENT>
Client idéal : <ICP approximatif>
Objectif : trouver 10 prospects B2B sourcés, scorer les meilleurs, créer le CRM local, préparer 3 drafts personnalisés en review queue, produire un digest Slack. 

Contraintes :
- ne fais aucun envoi externe ;
- n’invente aucun décideur ni email ;
- cite les sources ;
- si une donnée manque, marque-la unknown/research_more ;
- sauvegarde tous les livrables dans workspace/prospect-runs/<date>-<slug>/ ;
- termine par un rapport de démo avec chemins des fichiers.
```

## Prompt court si tu veux improviser devant eux

```text
@Hermes Orchestra, lance une démo end-to-end pour <ENTREPRISE PARTENAIRE> : construis l’ICP, trouve des prospects sourcés, score-les, mets à jour le CRM, prépare des messages personnalisés en review queue et fais un digest. Aucun envoi externe. Qualité et preuves avant volume.
```

## Ce qui doit se passer pour une autre entreprise

1. Créer ou inférer un brief partenaire.
2. Produire un ICP spécifique.
3. Lancer `prospect-discovery` sur le marché cible.
4. Détecter signaux et pains.
5. Scorer fit × intention × timing.
6. Enrichir seulement si domaine/personne fiables.
7. Écrire un run dans `workspace/prospect-runs/<date>-<partner>/`.
8. Synchroniser `workspace/crm/`.
9. Générer 3 à 5 drafts dans `workspace/review-queue/pending/`.
10. Produire un digest dans `workspace/reports/` et Slack.

## Limite honnête

Un run nouveau avec recherche web réelle peut prendre plusieurs minutes et dépendre de la qualité des sources disponibles. Pour une démo courte, utiliser Wella comme scénario stable. Pour montrer la généricité, lancer une mini-démo sur 3 à 5 prospects avec une autre boîte plutôt qu’un run complet 20 leads.

## Exemple concret de mini-démo rapide

```text
@Hermes Orchestra, mini-démo générique : prends Notion comme société partenaire vendant un workspace collaboratif aux startups SaaS françaises. Trouve 5 prospects B2B sourcés en France, score-les, prépare 2 drafts en review queue, puis donne un digest. Aucun envoi externe.
```

## Critère de succès

L’évaluateur doit voir que :

- Wella n’est qu’un dataset préparé ;
- la logique est réutilisable ;
- les skills sont génériques ;
- le profil sait passer d’un brief à un pipeline ;
- l’agent reste prudent : pas de source = pas de claim, pas de validation = pas d’envoi.
