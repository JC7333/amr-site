# Cartographie sectorielle finance — Template Finance & Comptable

Ce document cartographie le mandat avec les règles sectorielles applicables aux activités financières et comptables en France et en Union européenne. Il complète les fiches AI Act et RGPD.

## DORA — Règlement (UE) 2022/2554

Le **Digital Operational Resilience Act** s'applique depuis le 17 janvier 2025 aux entités financières définies à l'article 2 (établissements de crédit, entreprises d'investissement, prestataires de services de paiement, établissements de monnaie électronique, sociétés de gestion, contreparties centrales, dépositaires centraux, certaines fintechs, etc.).

Les obligations clés couvertes par le mandat :

- **Article 5 — Gestion du risque TIC** : l'organisation doit cadrer le risque informatique, dont le déploiement d'un agent IA fait partie. Le mandat AMR documente le périmètre, les restrictions et les seuils de supervision, ce qui contribue à la cartographie des risques TIC.
- **Article 19 — Notification d'incident majeur** : en cas d'incident classé majeur selon les critères DORA (continuité, données, finance), notification à l'autorité compétente. Le mandat documente les `revocation.immediate_triggers` qui incluent l'incident de sécurité.
- **Article 24 — Tests de résilience opérationnelle** : programme de tests régulier sur les systèmes critiques. Un agent en première ligne crédit ou LCB-FT entre dans ce périmètre.
- **Articles 28 à 44 — Gestion des prestataires tiers critiques TIC** : les fournisseurs de modèles LLM et d'infrastructure d'agent peuvent être qualifiés comme prestataires tiers TIC. Le mandat précise `agent.provider`, `agent.model.family`, `agent.model.version` et `agent.model.hosted_in` pour permettre cette traçabilité.

L'**ACPR** est l'autorité compétente en France pour le contrôle DORA des entités sous sa supervision.

**À VALIDER PAR JURISTE** : l'inclusion exacte d'une fintech dans le périmètre DORA dépend de son statut réglementaire (établissement de paiement, prestataire de services sur actifs numériques, etc.). Une entité hors périmètre DORA reste néanmoins exposée à des exigences équivalentes lorsqu'elle est prestataire d'une entité dans le périmètre.

## LCB-FT — Code monétaire et financier, articles L.561-1 et suivants

La lutte contre le blanchiment et le financement du terrorisme s'applique aux entités assujetties listées à l'article L.561-2, qui couvre notamment les établissements de crédit, les sociétés de financement, les établissements de paiement, les fintechs, les experts-comptables, les commissaires aux comptes, et certains intermédiaires financiers.

Articles clés cartographiés par le mandat :

- **L.561-2** : qualification d'entité assujettie. À renseigner dans `principal.sector_status.lcb_ft_scope`.
- **L.561-4-1** : obligation de vigilance à l'égard de la clientèle, qui couvre l'identification (KYC), l'évaluation du risque et le suivi de la relation d'affaires.
- **L.561-10** : vigilance complémentaire pour les relations à risque élevé (personnes politiquement exposées, juridictions à risque).
- **L.561-15** : déclaration de soupçon à Tracfin. **Cette déclaration est exclusivement humaine.** Le mandat AMR interdit l'émission de token pour cette action via `human_only_mandatory.actions: ["declaration_soupcon_tracfin"]`.
- **L.561-12** : conservation des documents et informations liés à la vigilance pendant 5 ans à compter de la fin de la relation d'affaires. Cette durée est reflétée dans `audit_trail.log_retention_days: 1825`.
- **L.561-32** : dispositif de contrôle interne. Le mandat constitue un élément documentaire du contrôle interne pour l'agent en première ligne LCB-FT.

L'**ACPR** est l'autorité de contrôle, **Tracfin** est le destinataire des déclarations de soupçon.

## Obligations comptables — Code de commerce et Plan Comptable Général

- **Article L.123-12 du Code de commerce** : toute personne physique ou morale ayant la qualité de commerçant doit procéder à l'enregistrement comptable des mouvements affectant son patrimoine. L'agent peut **proposer** des écritures, jamais les **inscrire** au grand livre.
- **Article L.123-22 du Code de commerce** : conservation des documents comptables et pièces justificatives pendant **10 ans** à compter de la clôture de l'exercice. Cette durée est reflétée dans la variante balanced (`log_retention_days: 3650`) pour les logs liés à des écritures.
- **Règlement ANC 2014-03 — Plan Comptable Général** : applicable aux entités hors normes IFRS. Définit les règles de comptabilisation, d'évaluation et de présentation des comptes.
- **IAS / IFRS** : applicables aux entités cotées et certaines entités consolidées au-dessus des seuils légaux (article L.233-24 Code de commerce, et pour les comptes consolidés article L.233-16). Le mandat ne préjuge pas du référentiel applicable, à renseigner par l'organisation.

**À VALIDER PAR JURISTE** : le référentiel comptable applicable (PCG ou IFRS) dépend de la taille, du statut et du périmètre de consolidation de l'entité. Une mauvaise qualification peut entraîner un redressement.

## Codes déontologiques applicables

- **Ordre des experts-comptables** : code de déontologie applicable aux experts-comptables et aux salariés sous leur responsabilité. Le secret professionnel et l'indépendance sont des piliers ; un agent qui partagerait des données client avec un tiers serait en infraction directe.
- **Compagnie nationale des commissaires aux comptes (CNCC)** : pour les entités auditées par un commissaire aux comptes, l'agent doit être documenté et son périmètre connu de l'auditeur.

## Code de la consommation — relations B2C

Pour les agents qui interagissent avec des consommateurs personnes physiques (BNPL, crédit à la consommation) :

- **Article L.121-1 du Code de la consommation** : interdiction des pratiques commerciales trompeuses ou agressives. Une décision automatisée non transparente peut être qualifiée de pratique trompeuse.
- **Article L.312-1 et suivants du Code de la consommation** : encadrement du crédit à la consommation, qui couvre le BNPL au-dessus de certains seuils. Devoir d'explication, vérification de la solvabilité (qui ne peut pas reposer exclusivement sur un score automatisé), droit de rétractation.

## Articulation avec les autres cadres

Le déploiement d'un agent finance se trouve à l'intersection de l'AI Act (haut risque pour scoring), du RGPD (article 22 décision automatisée), de DORA (résilience opérationnelle) et de la LCB-FT (vigilance). Cette accumulation justifie le positionnement tarifaire haut du template (3 500 à 5 000 €) et la durée de validité courte (6 mois) du mandat. Le secteur évolue vite, les autorités sont actives, la jurisprudence se construit.

**À VALIDER PAR JURISTE** : toute adaptation du mandat à un cas d'usage précis doit être revue par un juriste spécialisé en droit financier et en droit du numérique. Le template fournit une base structurée, pas une qualification individuelle.
