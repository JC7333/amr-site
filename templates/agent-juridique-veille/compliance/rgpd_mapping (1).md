# Cartographie RGPD — Agent Juridique & Veille

Référence : **Règlement (UE) 2016/679** (RGPD) et **Loi Informatique et Libertés** modifiée (loi n° 78-17 du 6 janvier 1978).

## Données traitées par un agent de veille

Un agent de veille juridique manipule plusieurs catégories de données personnelles, souvent sans que cela soit perçu comme tel. La cartographie ci-dessous distingue les flux principaux.

### 1. Données issues de la jurisprudence publiée

Les décisions de justice publiques nomment, par construction, les parties (demandeur, défendeur, magistrats, avocats). Ce sont des **données personnelles** au sens de l'article 4 du RGPD, même si elles sont publiques.

Depuis 2019, la pseudonymisation des décisions de justice est progressivement déployée par la Cour de cassation et le Conseil d'État (loi n° 2019-222 du 23 mars 2019, articles 33 et 34, et décret n° 2020-797). Mais toutes les décisions ne sont pas encore pseudonymisées au moment de leur publication, en particulier les décisions des cours d'appel et des tribunaux de première instance accessibles via Légifrance ou des bases sectorielles.

**Conséquence** : un agent qui consomme de la jurisprudence brute traite des données nominatives de tiers qui n'ont pas consenti à ce traitement.

### 2. Données des utilisateurs internes

L'agent dialogue avec des juristes, des avocats, des collaborateurs. Les requêtes, les feedbacks, les fiches générées sont attachées à un utilisateur identifié dans le système d'information. Ces traces sont des **données personnelles des collaborateurs**.

### 3. Données de dossiers clients (cas du cabinet d'avocats)

Si l'agent est utilisé en cabinet et qu'il accède à des éléments de dossiers clients pour qualifier des alertes contextuelles, il traite des **données personnelles des clients du cabinet et des parties à leurs dossiers**, parfois des **catégories particulières** au sens de l'article 9 (santé, opinions politiques, infractions).

Ce flux est le plus risqué. Il est déconseillé sans cloisonnement strict et sans validation explicite de l'associé responsable.

## Articles applicables et mapping vers le mandat

### Article 5 — Principes

- **Licéité, loyauté, transparence (art. 5.1.a)** : la base légale doit être documentée pour chaque type de traitement (voir article 6 ci-dessous).
- **Limitation des finalités (art. 5.1.b)** : la finalité du traitement est explicitement définie dans `agent.purpose` du mandat (« assistance aux juristes humains, sans qualification juridique finale autonome »). L'utilisation pour entraîner un modèle tiers est interdite (`restrictions.forbidden_actions`).
- **Minimisation (art. 5.1.c)** : les champs autorisés sont limitativement énumérés (`permissions.read.fields_allowed`) et les champs interdits sont nommés (`permissions.read.fields_forbidden`).
- **Exactitude (art. 5.1.d)** : la chaîne SHA-256 garantit l'intégrité des fiches produites et des décisions de classification ; toute modification ultérieure laisse une trace.
- **Limitation de conservation (art. 5.1.e)** : les durées sont définies dans `data_access.retention_days` (1825 jours pour les synthèses publiées internes, 365 jours pour les fiches brutes et les logs d'interrogation).
- **Intégrité et confidentialité (art. 5.1.f)** : `data_access.cross_tenant_isolation: strict` impose un cloisonnement entre dossiers et clients.
- **Responsabilité (art. 5.2)** : le mandat lui-même, signé par le responsable habilité, matérialise l'accountability.

### Article 6 — Bases légales applicables

Plusieurs bases sont envisageables et le mandat les laisse explicitement à valider au cas par cas :

- **Article 6.1.e — Mission d'intérêt public** : applicable pour la veille réglementaire d'un opérateur réglementé qui doit suivre les évolutions législatives pour respecter ses obligations sectorielles (banque, assurance, énergie, télécoms).
- **Article 6.1.f — Intérêt légitime** : applicable pour la veille de service d'un cabinet d'avocats ou d'une direction juridique, sous réserve d'un test de mise en balance documenté et d'un droit d'opposition pour les personnes nommées dans la jurisprudence.
- **Article 6.1.b — Exécution d'un contrat** : applicable pour la production de fiches commandées par un client identifié dans le cadre d'une mission contractuelle.

**À VALIDER PAR JURISTE** : la base légale retenue doit être documentée dans le registre des activités de traitement de l'organisation et figurer dans la notice d'information.

### Article 9 — Catégories particulières de données

Les décisions de justice contiennent fréquemment des informations relatives à la **santé**, aux **infractions pénales**, aux **opinions politiques ou syndicales**, à la **vie sexuelle**, aux **convictions religieuses**.

L'article 9.2.f autorise le traitement « nécessaire à la constatation, à l'exercice ou à la défense d'un droit en justice ». L'article 9.2.g autorise le traitement nécessaire pour des « motifs d'intérêt public important ».

**Position du template** : la veille jurisprudentielle relève de l'une de ces deux exceptions selon la finalité concrète du traitement, à documenter dans le mandat (champ `compliance_mapping.rgpd.art_9`).

### Article 22 — Décisions automatisées individuelles

Pour de la veille pure, l'article 22 ne s'applique généralement pas : l'agent ne prend pas de décision individuelle affectant une personne. Il produit des synthèses qualifiées par un humain.

L'article 22 redevient applicable si l'agent **score** des personnes nommées dans la jurisprudence (par exemple, scoring d'un magistrat sur sa propension à condamner). Cet usage est interdit dans toutes les variantes du template (`restrictions.prohibited_criteria_in_alerts`).

### Article 28 — Sous-traitance

Le fournisseur du modèle LLM est presque toujours un **sous-traitant** au sens de l'article 28. Un contrat de sous-traitance conforme doit être signé, comportant les clauses obligatoires de l'article 28.3. L'utilisation d'un fournisseur sans clauses de sous-traitance signées rend le traitement illicite.

Le mandat impose dans `agent.llm_provider_compliance` la résidence des données en UE et la signature d'un accord article 28. Ces points sont des préconditions à la signature du mandat.

### Article 30 — Registre des activités de traitement

Le mandat AMR ne dispense pas l'organisation de tenir son registre RGPD. Il s'y intègre comme une fiche de traitement supplémentaire, avec un identifiant dans le registre interne.

### Article 32 — Sécurité

Le mandat impose plusieurs garanties techniques :

- Chaînage SHA-256 des mandats et des actions (`tamper_evidence: sha256_chain`).
- Cloisonnement strict entre dossiers et clients (`cross_tenant_isolation: strict`).
- Journalisation détaillée (`audit_trail.logged_events`).
- Lecture seule des journaux par un cercle restreint (`audit_trail.access_log`).

### Article 35 — Analyse d'impact (DPIA)

Une DPIA est obligatoire si le traitement présente un risque élevé pour les droits et libertés des personnes (article 35.1). Les lignes directrices CNIL sur les traitements à risque élevé incluent notamment :

- Le **traitement à grande échelle** de données issues de jurisprudence nominative.
- Le traitement de **catégories particulières** au sens de l'article 9 si la finalité dépasse le strict suivi réglementaire.
- L'utilisation **innovante de technologies** (l'IA générative est citée explicitement par la CNIL dans ses recommandations 2024-2026).

**Position du template** : une DPIA est **présumée requise** pour tout déploiement de cet agent à l'échelle d'une direction juridique d'ETI ou d'un cabinet d'avocats traitant un volume conséquent de jurisprudence.

### Articles 13 et 14 — Information des personnes

L'organisation déployeuse doit informer :

- Ses **collaborateurs** (article 13) que leurs interactions avec l'agent sont journalisées et utilisées à des fins de supervision.
- Les **personnes nommées dans la jurisprudence** (article 14) si l'organisation les contacte ou prend une décision les affectant. En pratique, cette information se limite aux cas où l'organisation tire de la jurisprudence un usage direct vis-à-vis d'une personne identifiée.

### Articles 15 à 22 — Droits des personnes

Les droits d'accès, de rectification, d'effacement, de limitation, d'opposition restent applicables. Un point opérationnel délicat : l'effacement d'une fiche stockée dans la chaîne SHA-256 ne peut être qu'une **invalidation** (le mandat est révoqué, la fiche est marquée comme retirée, mais l'empreinte cryptographique demeure pour préserver l'intégrité de la chaîne). Cette approche est compatible avec l'article 17 sous réserve de documentation.

## Articulation avec la Loi Informatique et Libertés

La loi n° 78-17 modifiée précise certains points français spécifiques :

- L'**article 6** précise les conditions de licéité.
- L'**article 88** rappelle les pouvoirs de la CNIL en matière d'IA.
- Les pouvoirs de contrôle et de sanction de la CNIL (jusqu'à 20 M€ ou 4 % du chiffre d'affaires mondial) s'exercent sur tout déploiement non conforme.

## Sanctions encourues

Article 83 du RGPD :

- Jusqu'à **10 M€ ou 2 %** du chiffre d'affaires mondial annuel (manquements de niveau 1 — articles 8, 11, 25 à 39, 42, 43).
- Jusqu'à **20 M€ ou 4 %** du chiffre d'affaires mondial annuel (manquements de niveau 2 — articles 5, 6, 7, 9, 12 à 22, 44 à 49, 58.1 et 58.2).

Au-delà du montant, la **réputation** d'un cabinet d'avocats ou d'une direction juridique est très exposée à un manquement RGPD lié à un usage d'IA mal encadré, particulièrement vis-à-vis du secret professionnel.

## Points à valider par un juriste ou DPO

- Vérifier la base légale retenue et documenter le test de mise en balance pour l'intérêt légitime. **À VALIDER PAR DPO.**
- Compléter le registre RGPD interne avec une fiche dédiée à l'agent.
- Lancer une DPIA si elle n'a pas été réalisée pour un traitement de portée comparable.
- Vérifier la conformité du contrat de sous-traitance avec le fournisseur du LLM et la résidence effective des données.
- Préparer la procédure de réponse aux demandes d'exercice de droits (articles 15 à 22) en intégrant la spécificité de la chaîne SHA-256 (invalidation plutôt qu'effacement strict).
- Articuler avec les **lignes directrices CNIL sur l'IA** publiées en 2024-2025 et les recommandations sectorielles éventuelles.
