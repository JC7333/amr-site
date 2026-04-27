# Cartographie sectorielle spécifique — Agent Juridique & Veille

L'agent de veille juridique opère à l'intersection de plusieurs cadres déontologiques et sectoriels qui s'ajoutent au RGPD et à l'AI Act. Cette fiche cartographie les principaux. Elle n'est pas exhaustive et doit être complétée selon le secteur exact du déployeur.

## 1. Profession d'avocat — RIN et Code de déontologie

Le **Règlement Intérieur National** (RIN) de la profession d'avocat encadre l'exercice professionnel. Trois articles sont directement pertinents pour le déploiement d'un agent IA en cabinet.

### Article 21.6.3 — Outils numériques

L'avocat qui utilise un outil numérique tiers (cloud, SaaS, prestataire de services) reste personnellement responsable du respect du secret professionnel et de la confidentialité des données client. Le mandat AMR matérialise cette responsabilité par :

- L'identification nominative du mandant (`principal.representative.full_name` + `bar_membership`).
- Le cloisonnement strict entre dossiers (`cross_tenant_isolation: strict`).
- L'interdiction explicite d'entraîner un modèle tiers sur les dossiers (`restrictions.forbidden_actions`).
- La possibilité de révoquer immédiatement le mandat en cas d'incident ou de mise à jour majeure du modèle.

### Article 21.6.4 — Confidentialité et secret professionnel

Le déploiement d'un outil tiers ne doit pas compromettre le secret professionnel. Le mandat impose des sources autorisées, des périmètres d'action explicites, et l'interdiction de transmettre toute information à un client externe sans validation humaine.

**Recommandation** : pour un cabinet, la variante `restrictive` du template est le point de départ par défaut. Elle limite l'agent aux sources publiques officielles, interdit toute synthèse thématique, et impose une validation humaine sur toutes les sorties.

### Code de déontologie (décret n° 2005-790 modifié)

L'article 1.3 impose la confidentialité. L'article 1.5 impose la diligence et la compétence. Un avocat qui produirait une note client à partir d'une synthèse d'agent sans la qualifier juridiquement engage sa responsabilité professionnelle. Le mandat l'oblige à valider explicitement avant toute diffusion.

### Secret professionnel — Article 226-13 du Code pénal

Le secret professionnel protège les informations confiées au juriste. Sa violation est punie d'un an d'emprisonnement et de 15 000 € d'amende. Un agent qui consommerait un dossier client sans cloisonnement et qui restituerait des éléments de ce dossier dans le contexte d'un autre client engage la responsabilité pénale du superviseur humain.

**Conséquence opérationnelle** : la liste des dossiers et clients exclus du périmètre de l'agent doit être tenue à jour et chargée dans le mandat avant chaque déploiement.

## 2. Banque-finance — ACPR et AMF

### Autorité de Contrôle Prudentiel et de Résolution (ACPR)

Pour un déploiement en établissement bancaire ou en compagnie d'assurance, l'agent de veille s'inscrit dans le dispositif de **conformité réglementaire** prévu par les articles L. 511-41-1 B et L. 511-55 du Code monétaire et financier.

L'ACPR a publié en 2020 un document de réflexion sur l'**explicabilité de l'IA dans le secteur financier**. Bien qu'il s'agisse d'une recommandation et non d'une obligation, les déploiements d'IA dans les fonctions de contrôle interne sont surveillés. Le mandat AMR fournit les éléments d'explicabilité et de traçabilité attendus.

Pour la **lutte contre le blanchiment et le financement du terrorisme** (LCB-FT), un agent de veille peut alimenter le dispositif d'alerte mais ne peut pas le remplacer. La décision finale d'alerter Tracfin reste humaine. Le mandat l'interdit explicitement (`permissions.write.actions_forbidden: notifier_autorite_de_controle`).

### Autorité des Marchés Financiers (AMF)

Pour un déploiement en société de gestion ou en conseil en investissement (CIF), l'agent de veille doit respecter le **Règlement général AMF** et la **doctrine AMF sur l'usage d'outils d'aide à la décision**. La position-recommandation DOC-2020-03 sur les techniques d'IA encadre l'usage de l'IA en gestion d'actifs.

Le mandat impose la traçabilité des sources et la non-substitution de l'agent à la décision d'investissement, qui reste humaine.

## 3. Santé — ARS et HAS

Pour un déploiement dans un établissement de santé ou auprès d'un professionnel de santé, l'agent de veille intersecte plusieurs cadres :

- L'**hébergement de données de santé (HDS)** au sens de l'article L. 1111-8 du Code de la santé publique impose un hébergeur certifié pour toute donnée de santé à caractère personnel. Si l'agent traite des décisions de justice santé contenant des données médicales identifiables, l'hébergement du registre AMR doit être HDS-certifié, ou les données doivent être anonymisées avant traitement.
- Les **recommandations HAS sur l'IA en santé** et les positions de la **Société Française de Santé Numérique** apportent des garde-fous additionnels.
- Pour les **professions médicales et paramédicales**, le secret médical (article L. 1110-4 du Code de la santé publique) impose un cloisonnement équivalent à celui du secret professionnel des avocats.

**Recommandation** : pour la santé, la variante `restrictive` du template est obligatoire et la validation par le DPO de l'établissement est non négociable.

## 4. Télécoms et numérique — ARCEP, ARCOM, ANSSI

### ARCEP

Pour un opérateur télécoms, la veille réglementaire couvre les évolutions du Code des postes et des communications électroniques, les décisions ARCEP, et les régulations européennes (BEREC, EECC).

### ARCOM

Pour un éditeur de plateforme intermédiaire au sens du **Digital Services Act** (Règlement UE 2022/2065), la veille couvre les obligations de transparence, les rapports annuels, et les recommandations de l'ARCOM.

### ANSSI

Pour un opérateur d'importance vitale (OIV) ou un opérateur de services essentiels (OSE) au sens de la **directive NIS2** transposée par la loi du 22 mai 2023, la veille couvre les obligations de cybersécurité, les notifications d'incident, et les recommandations ANSSI.

L'agent de veille peut alimenter la chaîne d'alerte mais ne peut pas s'y substituer. La notification d'un incident à l'ANSSI ou au CSIRT compétent reste humaine.

## 5. Énergie — CRE et MTE

Pour un opérateur du secteur de l'énergie, la veille couvre :

- Le Code de l'énergie et ses évolutions.
- Les décisions de la **Commission de Régulation de l'Énergie** (CRE).
- Les directives européennes (EU ETS, RED III, Fit for 55).
- Les obligations sectorielles spécifiques (effacement, mécanisme de capacité, certificats d'économies d'énergie).

Aucune particularité majeure additionnelle au cadre général du template, mais la liste des sources autorisées doit être étendue aux publications CRE et MTE.

## 6. OHADA — entreprises présentes en Afrique francophone

Pour les organisations dont l'activité couvre les pays membres de l'**OHADA** (Organisation pour l'Harmonisation en Afrique du Droit des Affaires), la veille couvre les Actes uniformes OHADA, la jurisprudence de la **Cour Commune de Justice et d'Arbitrage** (CCJA), et les évolutions des droits nationaux des États membres.

Le mandat permet d'étendre `scope.jurisdictions_allowed` à `[FR, EU, OHADA]` après validation par un juriste OHADA.

## 7. Articulation avec les autres cadres

### Code du travail

Si l'agent peut amener à des décisions affectant des travailleurs (suivi de jurisprudence prud'homale qui guide une décision de licenciement, par exemple), les obligations de **consultation du CSE** s'appliquent (articles L. 2312-38 et L. 2312-26 du Code du travail). De plus, le déploiement bascule potentiellement en **Annexe III point 4 de l'AI Act** (haut risque), ce qui change radicalement le cadre.

### Code de la consommation

Si l'agent produit des contenus diffusés à des clients consommateurs (newsletter de cabinet, fiches publiées), les obligations d'information loyale et de pratiques commerciales non trompeuses s'appliquent.

### Code de propriété intellectuelle

L'agent qui consomme des bases jurisprudentielles ou doctrinales sous licence (Dalloz, LexisNexis, Lamyline) doit respecter les conditions générales de ces fournisseurs, qui interdisent souvent l'usage en aval pour entraîner des modèles tiers ou pour générer des produits dérivés concurrents.

## Points à valider par un juriste

- Identifier précisément le ou les secteurs concernés et appliquer les obligations correspondantes. **À VALIDER PAR JURISTE.**
- Compléter `scope.monitored_sources_allowed` avec les sources sectorielles spécifiques.
- Compléter `compliance_mapping.sectoriel_specifique` avec les références applicables.
- Pour les avocats, vérifier l'articulation avec les usages du barreau local et la position du bâtonnier.
- Pour les opérateurs réglementés, articuler avec le dispositif de contrôle interne existant.
- Vérifier les conditions de licence des bases tierces consommées (Dalloz, LexisNexis, Lamyline, Doctrine).
