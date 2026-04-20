# Guide de déploiement — Agent RH Recrutement

Ce guide résume les étapes de mise en production du template dans un registre AMR connecté à un ATS. Il ne remplace pas une revue interne (DPO, juridique, CSE).

## Préalables

- Un registre AMR installé (Tier 0 open-source ou Tier 1 mandate-gated).
- Un ATS (ou l'outil RH cible) capable d'exposer un webhook ou une API de lecture des candidatures.
- Un agent IA déjà déployé en interne ou fourni par un prestataire, avec un identifiant stable.
- Un responsable hiérarchique habilité à signer le mandat (DRH, représentant légal).
- Un DPO ou référent RGPD disponible pour relire le mandat avant signature.

## Étape 1 — Adapter le template maître

1. Ouvrir `mandate.yaml`.
2. Remplacer toutes les valeurs entre `< >` par les valeurs de l'organisation.
3. Choisir le profil de base parmi les trois exemples fournis (`permissif`, `restrictif`, `équilibré`) et fusionner avec le template maître si besoin.
4. Vérifier la cohérence des volumes (`max_volume_per_day`) avec le flux réel de candidatures.
5. Faire relire par le DPO.

## Étape 2 — Revue juridique interne

- Vérifier l'applicabilité du régime « haut risque » de l'AI Act (Annexe III, point 4).
- Documenter le test de mise en balance pour l'intérêt légitime (RGPD, article 6(1)(f)).
- Décider si une analyse d'impact (DPIA, article 35) est nécessaire.
- Identifier les conventions collectives et accords d'entreprise applicables.
- Valider la durée de conservation des journaux au regard de la prescription applicable.

## Étape 3 — Information des parties prenantes

- **Candidats** : mettre à jour la notice d'information (RGPD, article 13 et Code du travail, article L.1221-9) pour mentionner l'existence et la nature de l'agent.
- **CSE** : consultation formelle si l'organisation en est dotée (Code du travail, articles L.2312-38 et L.2312-26).
- **Recruteurs** : formation obligatoire aux biais algorithmiques, à la supervision humaine et aux droits des candidats. Consigner la formation dans un registre interne.

## Étape 4 — Chargement du mandat dans AMR

1. Valider le YAML avec un parseur strict (`python -c "import yaml; yaml.safe_load(open('mandate.yaml'))"`).
2. Signer le mandat : signature interne ou signature électronique eIDAS qualifiée selon la politique de l'organisation.
3. Charger dans le registre AMR via l'outil `create_mandate`.
4. Vérifier la présence dans la chaîne avec `audit_mandate_chain`.
5. Configurer l'agent pour qu'il appelle `verify_mandate` avant toute action sensible.

## Étape 5 — Tests de bout en bout

Avant la mise en production réelle :

- **Test de périmètre** : soumettre une candidature hors périmètre autorisé, vérifier le refus.
- **Test de volume** : simuler un pic au-delà de `max_volume_per_day`, vérifier le blocage et l'alerte.
- **Test de supervision** : simuler un score bas, vérifier le déclenchement de la revue humaine obligatoire.
- **Test de révocation** : révoquer le mandat, vérifier que l'agent cesse immédiatement d'agir.
- **Test d'audit** : exporter les journaux sur une période courte, vérifier l'intégrité SHA-256.

## Étape 6 — Checklist de validation avant mise en prod

- [ ] Mandat relu et signé par le représentant habilité.
- [ ] DPO consulté, DPIA réalisée si nécessaire.
- [ ] CSE informé et, le cas échéant, consulté.
- [ ] Notice candidats mise à jour et publiée.
- [ ] Formation des recruteurs effectuée et tracée.
- [ ] Registre des traitements mis à jour.
- [ ] Contrat de sous-traitance signé avec le fournisseur du modèle (RGPD, article 28).
- [ ] Procédure de gestion des demandes d'exercice de droits opérationnelle.
- [ ] Tests de bout en bout passés.
- [ ] Date de revue du mandat calée dans un calendrier (tous les 3 à 12 mois selon profil).

## Points d'attention critiques

- **La supervision humaine doit être effective**, pas symbolique. Un reviewer qui valide en masse sans lire les cas sensibles ne remplit pas l'obligation de l'article 14 de l'AI Act.
- **Toute mise à jour majeure du modèle LLM** doit déclencher la révocation du mandat en cours et la signature d'un nouveau mandat. Un modèle n'est pas une variable libre.
- **Les transferts hors UE** sont interdits par défaut dans le template. Si le fournisseur du modèle les nécessite, encadrement par clauses contractuelles types et analyse de transfert spécifique (RGPD, articles 44 à 49).
- **La chaîne d'audit est inutile si personne ne la lit.** Prévoir une revue périodique par l'audit interne, a minima trimestrielle.
