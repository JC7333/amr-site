# Règles sectorielles — Infrastructure & Datacenter

En complément de l'AI Act et du RGPD, le déploiement d'un agent IA en datacenter doit respecter le cadre NIS2, les standards de sécurité de l'information et les normes propres à l'infrastructure.

## NIS2 — Directive (UE) 2022/2555

### Transposition française

**Loi n° 2024-364 du 22 avril 2024** portant diverses dispositions d'adaptation au droit de l'Union européenne en matière d'économie, de finances, de transition écologique, de droit pénal, de droit social et en matière agricole. Décrets d'application en cours de publication. **À SUIVRE.**

### Champ d'application

Les fournisseurs de services d'informatique en nuage, les fournisseurs de centres de données, les fournisseurs de réseaux de diffusion de contenu et les opérateurs de points d'échange internet sont visés à l'**Annexe I** de la Directive (entités essentielles).

L'agent décrit dans ce template intervient dans des activités qui, en cas de défaillance, peuvent affecter la disponibilité d'un service essentiel. Les obligations NIS2 s'appliquent au déployeur.

### Article 21 — Mesures de gestion du risque

Les entités essentielles et importantes adoptent des mesures techniques, opérationnelles et organisationnelles « appropriées et proportionnées » pour gérer les risques pesant sur la sécurité des réseaux et systèmes d'information.

Le mandat AMR documente une partie de ces mesures :

- Politique de sécurité (mandat signé, périmètre clair).
- Gestion des incidents (`audit_trail`, `mandatory_review_triggers`).
- Continuité d'activité (`expiration.revocation`).
- Sécurité de la chaîne d'approvisionnement (champ `agent.provider`).
- Politiques de contrôle d'accès (`scope`, `restrictions.human_only_mandatory`).

### Article 23 — Notification d'incident significatif

Délais à respecter :

1. **Alerte précoce** : sans retard injustifié et au plus tard **24 heures** après en avoir eu connaissance, à l'autorité compétente (en France : ANSSI).
2. **Notification d'incident** : sans retard injustifié et au plus tard **72 heures**.
3. **Rapport final** : au plus tard **un mois** après la notification d'incident.

Le journal d'audit AMR (`tamper_evidence: sha256_chain`, événements `tentative_action_hors_scope`, `refus_emission_token_action`) facilite la qualification rapide.

### Article 34 — Sanctions

Pour les entités essentielles : amendes administratives jusqu'à **10 M€ ou 2 % du chiffre d'affaires mondial annuel**, le montant le plus élevé étant retenu.

Pour les entités importantes : jusqu'à **7 M€ ou 1,4 %**.

## ISO/IEC 27001:2022 — Sécurité de l'information

Les contrôles particulièrement pertinents pour un agent d'infrastructure :

- **A.5.23** — Sécurité de l'information pour l'utilisation de services en nuage.
- **A.8.2** — Droits d'accès privilégiés. Le mandat AMR formalise ces droits pour un agent IA.
- **A.8.16** — Activités de surveillance.
- **A.8.34** — Protection des systèmes d'information durant les tests d'audit.
- **A.5.24 à A.5.27** — Gestion des incidents.

Un système de management de la sécurité de l'information (SMSI) certifié ISO 27001 doit intégrer la gouvernance des agents IA. Le mandat AMR fournit la documentation traçable demandée par les auditeurs.

## ISO 22301:2019 — Continuité d'activité

Particulièrement pertinent pour un opérateur de datacenter :

- **Clause 8.4** — Procédures de continuité d'activité. Un agent qui exécute des actions doit être inclus dans le plan de continuité (que se passe-t-il si l'agent ou son fournisseur tombe ?).
- **Clause 8.5** — Exercices et tests. Les tests doivent inclure le scénario « révocation immédiate du mandat de l'agent ».

Le champ `expiration.revocation.immediate_triggers` du mandat liste les déclencheurs.

## ANSI/TIA-942-C — Telecommunications infrastructure standard for data centers

Le standard TIA-942-C définit quatre niveaux de **tier** (Rated-1 à Rated-4) selon la disponibilité, la redondance et la tolérance aux pannes.

Le template recommande d'**exclure par défaut** les environnements de production critique tier III et tier IV (`excluded_environments: production_critique_tier_iii`, `production_critique_tier_iv`). Une intégration sur ces tiers nécessite une analyse de risque dédiée et probablement un mandat plus restrictif.

## Référentiels sectoriels complémentaires

### Hébergeurs de données de santé (HDS)

Si l'opérateur est certifié **HDS** au titre du référentiel français de certification des hébergeurs de données de santé, des obligations renforcées s'appliquent. Un agent IA touchant à des systèmes hébergeant des données de santé doit faire l'objet d'une analyse spécifique. **Hors périmètre de ce template v1 ; un template dédié santé est prévu dans la feuille de route.**

### SecNumCloud (ANSSI)

Pour les opérateurs visés par la qualification SecNumCloud, des exigences spécifiques s'appliquent au déploiement de composants logiciels tiers, dont les agents IA. **À VALIDER PAR L'ANSSI** au cas par cas.

### DORA — Règlement (UE) 2022/2554

Pour les opérateurs hébergeant des entités financières, le règlement DORA impose des obligations sur la résilience opérationnelle numérique. Un agent IA opérant sur l'infrastructure d'une banque ou d'un assureur entre dans le périmètre. **À VALIDER PAR JURISTE.**

## Engagements contractuels vis-à-vis des clients hébergés

Beaucoup d'opérateurs ont des engagements de SLA et de transparence vis-à-vis de leurs clients. Le déploiement d'un agent qui touche à des systèmes hébergeant des charges client doit être :

- soit explicitement autorisé par le contrat-cadre,
- soit notifié au client préalablement à la mise en production.

Le champ `audit_trail.log_access` du template inclut explicitement la possibilité d'un accès `client_heberge_sur_perimetre_le_concernant`.

## Certifications professionnelles

Certaines certifications opérateur (Uptime Institute, BICSI, etc.) impliquent des engagements sur la gouvernance opérationnelle. **À VÉRIFIER** en amont du déploiement avec le responsable certification interne.
