# Cartographie AI Act — Agent RH Recrutement

Référence : **Règlement (UE) 2024/1689** du Parlement européen et du Conseil établissant des règles harmonisées concernant l'intelligence artificielle.

## Classification

Un système d'IA utilisé pour le recrutement, la sélection ou l'évaluation des candidats relève de l'**Annexe III, point 4** du Règlement. À ce titre, il est classé **système à haut risque**.

> Annexe III, point 4 : « Emploi, gestion des travailleurs et accès à l'emploi indépendant », en particulier (a) les systèmes destinés à être utilisés pour le recrutement ou la sélection de personnes physiques, notamment pour publier des offres ciblées, analyser et filtrer les candidatures, et évaluer les candidats.

Cette classification déclenche l'ensemble des obligations du Chapitre III, Section 2 du Règlement.

## Obligations mappées dans `mandate.yaml`

### Article 12 — Tenue de registres

Le système doit enregistrer automatiquement les événements pertinents pendant toute la durée de vie du système à haut risque.

Dans le template : section `audit_trail.logged_events` et `log_retention_days`. La chaîne SHA-256 (`tamper_evidence`) garantit l'intégrité des traces.

### Article 13 — Transparence et information des utilisateurs

Le système doit fournir aux déployeurs des informations claires et complètes sur son fonctionnement.

Dans le template : section `agent.purpose` et `compliance_mapping`. La notice d'information aux candidats reste à la charge du déployeur (cf. `rgpd_mapping.md`).

### Article 14 — Supervision humaine

Les systèmes à haut risque doivent être conçus de façon à permettre une supervision humaine effective, avec la possibilité d'interrompre ou d'annuler une décision.

Dans le template : section `human_oversight` entière. Trois régimes possibles — `human_in_the_loop_strict`, `human_in_the_loop`, `human_on_the_loop` — avec des déclencheurs obligatoires de revue humaine.

### Article 26 — Obligations des déployeurs

Le déployeur doit utiliser le système conformément à la notice, assurer la supervision humaine, tenir les journaux, et informer les personnes concernées lorsqu'il est décidé ou aidé à décider à leur sujet.

Dans le template : cadré par `principal.representative`, `human_oversight.reviewer_profile`, `audit_trail`, `expiration.revocation`.

## Calendrier d'application

Les obligations relatives aux systèmes à haut risque de l'Annexe III s'appliquent à partir du **2 août 2026**, conformément à l'article 113 du Règlement.

Un report partiel via le paquet dit « Digital Omnibus » est discuté au niveau européen à la date de rédaction de ce template. **À suivre au regard des trilogues en cours.** Le mandat reste valable dans les deux hypothèses.

## Sanctions encourues

Article 99 du Règlement : jusqu'à **35 M€ ou 7 % du chiffre d'affaires mondial annuel** pour les manquements les plus graves (pratiques d'IA interdites — article 5). Jusqu'à **15 M€ ou 3 %** pour les manquements aux obligations des systèmes à haut risque.

## Points à valider par un juriste

- Vérifier si le déploiement prévu relève effectivement de l'Annexe III point 4 dans le cas d'usage précis (certains outils purement descriptifs peuvent en être exclus). **À VALIDER PAR JURISTE.**
- Vérifier la qualité de « déployeur » vs « fournisseur » au sens du Règlement (articles 3 et 25).
- S'assurer que l'évaluation de conformité et le marquage CE du système fourni ont été réalisés en amont par le fournisseur du modèle.
