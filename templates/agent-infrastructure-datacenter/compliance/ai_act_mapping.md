# Cartographie AI Act — Agent Infrastructure & Datacenter

Référence : **Règlement (UE) 2024/1689** du Parlement européen et du Conseil établissant des règles harmonisées concernant l'intelligence artificielle.

## Classification potentielle

Un système d'IA utilisé dans la gestion ou l'exploitation d'infrastructures critiques peut relever de l'**Annexe III, point 2** du Règlement.

> Annexe III, point 2 : « Infrastructures critiques », en particulier les systèmes d'IA destinés à être utilisés en tant que composants de sécurité dans la gestion et l'exploitation des infrastructures numériques critiques, du trafic routier ou de la fourniture d'eau, de gaz, de chauffage ou d'électricité.

L'applicabilité dépend du périmètre exact de l'agent et de la qualification de l'infrastructure au sens du droit applicable. **À VALIDER PAR JURISTE.** Un agent qui se borne à produire des rapports SLA en lecture seule peut ne pas être considéré comme « composant de sécurité » ; un agent qui exécute des changes ou ouvre des tickets prioritaires y entre plus probablement.

Si la classification haut risque est retenue, l'ensemble des obligations du Chapitre III, Section 2 du Règlement s'applique.

## Obligations mappées dans `mandate.yaml`

### Article 12 — Tenue de registres

Le système doit enregistrer automatiquement les événements pertinents pendant toute la durée de vie du système à haut risque.

Dans le template : section `audit_trail.logged_events` et `log_retention_days`. La chaîne SHA-256 (`tamper_evidence: sha256_chain`) garantit l'intégrité des traces. Les événements `emission_token_action` et `refus_emission_token_action` sont spécifiquement ajoutés pour tracer la couche d'enforcement AMR.

### Article 13 — Transparence et information des déployeurs

Le système doit fournir aux déployeurs des informations claires et complètes sur son fonctionnement et ses limites.

Dans le template : section `agent.purpose`, `scope.excluded_processes`, `restrictions.human_only_mandatory`. Le déployeur (l'opérateur de datacenter) sait précisément ce que l'agent peut et ne peut pas faire avant de signer le mandat.

### Article 14 — Supervision humaine

Les systèmes à haut risque doivent être conçus de façon à permettre une supervision humaine effective, avec la possibilité d'interrompre ou d'annuler une décision.

Dans le template : section `human_oversight` entière. Trois régimes possibles — `human_in_the_loop_strict`, `human_in_the_loop`, `human_on_the_loop` — avec des déclencheurs obligatoires. Les actions critiques (`couper_alimentation_baie_production`, `repondre_seul_a_un_incident_sev1`, etc.) sont placées dans `restrictions.human_only_mandatory` : le runtime AMR refuse l'émission de token même si le mandat est actif.

### Article 26 — Obligations des déployeurs

Le déployeur doit utiliser le système conformément à la notice, assurer la supervision humaine, tenir les journaux, et notifier les incidents.

Dans le template : cadré par `principal.representative`, `human_oversight.reviewer_profile`, `audit_trail`, `expiration.revocation`. La couverture 24/7 (`on_call_coverage: "24_7"`) est obligatoire pour ce template, cohérente avec la nature opérationnelle du domaine.

## Calendrier d'application

Les obligations relatives aux systèmes à haut risque de l'Annexe III s'appliquent à partir du **2 août 2026**, conformément à l'article 113 du Règlement.

Un report partiel via le paquet dit « Digital Omnibus » est en discussion au niveau européen à la date de rédaction de ce template. Les trilogues sont en cours, le report n'est pas arrêté en droit positif. Hypothèses publiques : report au 2 décembre 2026 ou au 2 décembre 2027 selon les versions débattues. **À SUIVRE.** Le mandat reste valable dans les deux scénarios — il s'applique dès la signature, indépendamment du calendrier réglementaire.

## Sanctions encourues

Article 99 du Règlement :
- Jusqu'à **35 M€ ou 7 % du chiffre d'affaires mondial annuel** pour les pratiques d'IA interdites (article 5).
- Jusqu'à **15 M€ ou 3 %** pour les manquements aux obligations sur systèmes à haut risque.
- Jusqu'à **7,5 M€ ou 1 %** pour la fourniture d'informations incorrectes aux autorités.

## Articulation avec NIS2

Les opérateurs de datacenter sont fréquemment des entités essentielles ou importantes au sens de la Directive (UE) 2022/2555. Les obligations AI Act et NIS2 se cumulent, ne se substituent pas. Un incident causé par un agent IA non encadré peut déclencher à la fois :

- une notification d'incident significatif à l'ANSSI au titre de l'article 23 NIS2 (délais : 24h pour l'alerte précoce, 72h pour la notification, 1 mois pour le rapport final) ;
- un signalement à l'autorité de surveillance du marché de l'IA au titre de l'article 73 AI Act (incident grave).

## Points à valider par un juriste

- Vérifier si le déploiement prévu relève effectivement de l'Annexe III point 2 dans le cas d'usage précis. Tous les agents NOC ne sont pas automatiquement « composants de sécurité ». **À VALIDER PAR JURISTE.**
- Vérifier la qualité de « déployeur » vs « fournisseur » au sens du Règlement (articles 3 et 25). Un opérateur de datacenter qui développe son propre agent est probablement les deux, ce qui cumule les obligations.
- S'assurer que l'évaluation de conformité et le marquage CE du système fourni ont été réalisés en amont si l'agent est acquis auprès d'un fournisseur tiers.
- Documenter l'analyse d'impact sur les droits fondamentaux (article 27) si la classification haut risque est retenue.
