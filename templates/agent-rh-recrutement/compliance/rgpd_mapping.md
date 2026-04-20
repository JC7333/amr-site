# Cartographie RGPD — Agent RH Recrutement

Référence : **Règlement (UE) 2016/679** (RGPD) et **Loi n° 78-17 du 6 janvier 1978 modifiée** (Loi Informatique et Libertés).

## Base légale — Article 6

Le template retient l'**intérêt légitime** (article 6(1)(f)) comme base légale par défaut. Cet intérêt consiste à gérer les candidatures reçues et à sélectionner les profils adaptés aux postes à pourvoir.

Le recours à l'intérêt légitime suppose la tenue d'un **test de mise en balance** documenté, qui justifie que l'intérêt du responsable de traitement ne prévaut pas de façon disproportionnée sur les droits et libertés des candidats. **À VALIDER PAR JURISTE** selon le contexte précis.

Dans le template : section `principal.legal_basis_gdpr` et référence `balancing_test_ref`.

## Information des candidats — Article 13

Les candidats doivent être informés, au plus tard au moment de la collecte de leurs données, de l'existence d'un traitement assisté par IA, de sa finalité, de sa base légale, de la durée de conservation, et de leurs droits.

**Le mandat ne dispense pas** de cette information ; il la rend auditable.

## Décision individuelle automatisée — Article 22

L'article 22 interdit, sauf exceptions, la décision produisant des effets juridiques ou affectant significativement la personne lorsqu'elle est fondée **exclusivement** sur un traitement automatisé.

Le template est conçu pour **ne pas tomber** sous l'article 22 : toute décision produisant un effet (rejet, proposition d'entretien, envoi de message) passe par une validation humaine effective, consignée dans le journal d'audit.

Dans le template : `human_oversight.mandatory_review_triggers` et champ `automated_decision_making_article_22: false` dans les exemples.

**Attention** : la CNIL considère que l'intervention humaine doit être *significative*, pas une simple validation automatique. Les reviewers doivent être formés (champ `reviewer_profile.training_required: true`) et avoir le pouvoir effectif de contredire la recommandation de l'agent.

## Analyse d'impact — Article 35

Le recrutement assisté par IA entre typiquement dans les cas où une analyse d'impact (DPIA) est requise : traitement à grande échelle de données personnelles, évaluation de personnes, nouveau type de technologie.

La CNIL a publié une liste des traitements pour lesquels une DPIA est requise (délibération n° 2018-327 du 11 octobre 2018). **À VALIDER** selon la nature exacte du déploiement.

Dans le template : champ `dpia_required: true` dans les exemples.

## Catégories particulières — Article 9

Les données de santé, d'origine raciale ou ethnique, d'opinions politiques, syndicales, religieuses, de vie ou d'orientation sexuelle sont des catégories particulières protégées. **Leur traitement par l'agent est interdit** (champ `data_access.special_categories_article_9: "non_autorise"` du template maître).

Corollaire : les champs CV susceptibles de révéler ces données (photo, date de naissance, situation familiale, état de santé) sont listés dans `fields_forbidden` et ne doivent pas être transmis à l'agent.

## Durée de conservation

Le template propose 90 jours pour les candidatures actives et 730 jours (2 ans) pour les candidatures conservées avec l'accord du candidat. Ces durées reflètent la **recommandation de la CNIL en matière de recrutement** ; elles doivent être validées au regard du référentiel applicable. **À VALIDER PAR JURISTE.**

## Droits des personnes — Articles 15 à 21

Le journal d'audit AMR facilite l'exercice des droits : accès (article 15), rectification (16), effacement (17), limitation (18), portabilité (20), opposition (21).

La procédure de réponse aux demandes reste à la charge du déployeur et ne doit pas excéder un mois (article 12(3)).

## Points à valider par un DPO

- Test de mise en balance pour l'intérêt légitime (article 6(1)(f)).
- Nécessité d'une DPIA formelle (article 35).
- Mise à jour du registre des activités de traitement (article 30).
- Contrat de sous-traitance avec le fournisseur du modèle (article 28) — en particulier sur les transferts hors UE (articles 44 à 49).
- Information des représentants du personnel si applicable (Code du travail, articles L.2312-38 et L.2312-26).
