# Template AMR — Agent RH Recrutement

Template de mandat prêt à l'emploi pour encadrer un agent IA déployé en assistance au recrutement (tri de CV, pré-qualification, prise de rendez-vous, rédaction d'offres, réponses candidats).

## Pour qui

- DRH et responsables recrutement d'ETI et grands comptes qui testent un agent IA interne ou tiers.
- DPO et compliance officers qui doivent cadrer un déploiement déjà en cours.
- Intégrateurs et cabinets de recrutement qui proposent des agents à leurs clients et doivent livrer une gouvernance traçable.

## Contexte

Depuis 2024, les outils de tri automatique de candidatures et d'entretien assisté par IA se multiplient. Le règlement européen sur l'intelligence artificielle (Règlement UE 2024/1689, dit « AI Act ») classe explicitement les systèmes d'IA utilisés pour le recrutement, la sélection et l'évaluation des candidats comme **à haut risque** (Annexe III, point 4). Cela déclenche des obligations lourdes : supervision humaine effective, tenue de registres, transparence vis-à-vis des personnes concernées, gestion documentée du risque.

En parallèle, le RGPD encadre la décision automatisée (article 22) et le Code du travail français impose la pertinence et la transparence des méthodes d'évaluation (articles L.1221-6 à L.1221-9).

Déployer un agent de recrutement sans mandat explicite et vérifiable, c'est laisser à la machine le soin de décider qui passe le premier filtre — sans piste d'audit opposable, sans borne juridique claire, sans point d'arrêt.

## Trois exemples de déploiement concret

1. **Tri de candidatures entrantes** : un agent lit les CV déposés sur un ATS, extrait compétences et expérience, propose un score de correspondance avec la fiche de poste. Aucune décision d'élimination n'est prise par l'agent seul ; le recruteur humain valide chaque rejet.
2. **Pré-qualification par échange écrit** : l'agent dialogue avec le candidat pour compléter le CV (disponibilité, prétentions, mobilité), consigne les réponses, et remonte un dossier structuré au recruteur.
3. **Rédaction et diffusion d'offres** : l'agent produit une offre à partir d'une fiche de poste interne, vérifie le respect des mentions légales obligatoires, publie sur les canaux autorisés. Aucune modification des critères de poste sans validation humaine.

## Ce que ce template fournit

- `mandate.yaml` : le mandat structuré prêt à charger dans un registre AMR, avec périmètre d'action, volumes maximum, restrictions explicites, seuils de supervision humaine, durée de validité, cartographie RGPD et AI Act.
- `examples/` : trois variantes (permissive, restrictive, équilibrée) commentées, pour s'adapter au niveau de maturité de l'organisation.
- `compliance/` : trois fiches courtes qui cartographient le mandat avec l'AI Act, le RGPD et les règles sectorielles RH françaises.
- `deploy_guide.md` : checklist de mise en production et points d'attention.

## Lien avec le pivot enforcement AMR

Ce template fournit la configuration de mandat que le tool MCP `issue_action_token` utilisera pour émettre les jetons d'action signés en Ed25519 lors du runtime. Le mandat décrit ce qui est autorisé ; le runtime AMR n'émet un token que si le mandat est actif et couvre l'action demandée dans son scope. Pas de mandat valide, pas de token, pas d'action possible.

C'est un verrou structurel avant l'acte, pas un audit après. Pour le recrutement, cela signifie qu'aucun envoi de réponse négative en masse, aucune modification d'offre publiée, aucune programmation d'entretien ne peut se déclencher si le mandat ne couvre pas explicitement cette catégorie d'action. La spécification d'émission est documentée dans `docs/token-issuance-spec.md` du registre AMR.

## Pourquoi c'est risqué sans mandat

Un agent de recrutement sans mandat documenté expose l'organisation à plusieurs risques concrets :

- **Sanctions AI Act** : jusqu'à 35 M€ ou 7 % du chiffre d'affaires mondial pour les manquements aux obligations sur systèmes à haut risque (AI Act, article 99).
- **Sanctions RGPD** : jusqu'à 20 M€ ou 4 % du chiffre d'affaires en cas de décision automatisée non encadrée (article 22) ou d'absence d'analyse d'impact (article 35).
- **Contentieux prud'homal** : un candidat écarté peut demander la communication des méthodes d'évaluation (Code du travail, article L.1221-9). Sans piste d'audit, la défense est fragilisée.
- **Atteinte réputationnelle** : un biais de tri révélé publiquement, sans gouvernance à exhiber, coûte plus cher qu'une amende.

Le mandat AMR ne supprime pas ces risques — il les **encadre** et les **documente** de manière opposable.

## Positionnement tarifaire indicatif

Template vendu en pack clé en main, entre **2 000 € et 5 000 €** selon le niveau d'adaptation :

- **Pack standard (2 000 €)** : les fichiers tels quels, licence d'usage interne, une heure d'accompagnement à la configuration.
- **Pack adapté (3 500 €)** : personnalisation du mandat aux conventions collectives et outils ATS de l'organisation.
- **Pack intégré (5 000 €)** : déploiement dans un runtime AMR Tier 1, connexion ATS, première revue de conformité.

Le template seul ne remplace pas le runtime mandate-gated (Tier 1 AMR, 350 €/mois) ni une validation par un juriste interne. Il pose la structure ; la décision reste humaine.

## À valider côté client avant déploiement

- Revue du mandat par le DPO et le service juridique.
- Information préalable des candidats (RGPD, article 13 ; Code du travail, article L.1221-9).
- Mise à jour du registre des traitements.
- Décision sur la nécessité d'une analyse d'impact (DPIA) au titre de l'article 35 RGPD.
