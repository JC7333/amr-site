# Guide de déploiement — Agent Infrastructure & Datacenter

Ce guide résume les étapes de mise en production du template dans un registre AMR connecté aux outils de monitoring, de ticketing et de change management. Il ne remplace pas une revue interne (RSSI, comité change management, audit interne).

## Préalables

- Un registre AMR installé (Tier 0 open-source ou Tier 1 mandate-gated avec émetteur de tokens `issue_action_token`).
- Un système de monitoring exposant ses métriques via API (Prometheus, Zabbix, ou propriétaire).
- Un outil de ticketing avec API d'écriture (Jira, ServiceNow, OTRS, ou propriétaire).
- Un agent IA déjà déployé en interne ou fourni par un prestataire, avec un identifiant stable.
- Un RSSI ou responsable sécurité disponible pour relire le mandat avant signature.
- Un comité de change management (CAB) actif si l'agent doit exécuter des changes préapprouvés.

## Étape 1 — Adapter le template maître

1. Ouvrir `mandate.yaml`.
2. Remplacer toutes les valeurs entre `< >` par les valeurs de l'organisation.
3. Choisir le profil de base parmi les trois exemples fournis (`permissif`, `restrictif`, `équilibré`) et fusionner avec le template maître si besoin.
4. Vérifier la cohérence des volumes (`max_volume_per_day`) avec le flux réel de métriques et de tickets.
5. Lister explicitement les sites couverts dans `scope.sites_covered`.
6. Lister explicitement les services autorisés au redémarrage dans `permissions.invoke.restart_non_critical_service.services_allowed`.
7. Faire relire par le RSSI.

## Étape 2 — Revue sécurité interne

- Vérifier l'applicabilité du régime « haut risque » de l'AI Act (Annexe III, point 2). Selon le périmètre exact, un agent purement « lecture seule » peut sortir du champ ; un agent qui exécute des changes y entre.
- Documenter le test de mise en balance pour l'intérêt légitime (RGPD, article 6(1)(f)).
- Mettre à jour la cartographie des actifs et des risques au sein du SMSI ISO 27001.
- Articuler avec le plan de continuité ISO 22301 : que se passe-t-il si l'agent ou son fournisseur tombe ?
- Vérifier la qualification NIS2 de l'organisation (entité essentielle ou importante) et les obligations de notification associées.

## Étape 3 — Validation par le comité change management

Si l'agent est habilité à exécuter des changes préapprouvés (`scope.business_processes: execution_change_preapprouve_hors_production`) :

- Établir la liste exhaustive des types de changes autorisés (référence catalogue interne).
- Définir les fenêtres de maintenance pendant lesquelles l'agent peut agir.
- Valider en CAB le mandat AMR au même titre qu'une procédure standard.
- Documenter la procédure de revoke immédiat en cas de change défaillant.

## Étape 4 — Information des parties prenantes

- **Techniciens et opérateurs** : information sur le déploiement de l'agent, sur les journaux qui seront exploités, et sur leurs droits.
- **Clients hébergés** : notification préalable si requise par le contrat-cadre, en particulier si l'agent peut toucher à des équipements partagés.
- **Représentants du personnel** : information ou consultation selon la nature du déploiement et la taille de l'organisation (Code du travail, articles L.2312-38 et L.2312-26).
- **Astreinte NOC** : briefing opérationnel sur les déclencheurs de revue humaine et la procédure de prise en main lors d'un escalade.

## Étape 5 — Chargement du mandat dans AMR

1. Valider le YAML avec un parseur strict (`python -c "import yaml; yaml.safe_load(open('mandate.yaml'))"`).
2. Signer le mandat : signature interne ou signature électronique eIDAS qualifiée selon la politique de l'organisation.
3. Charger dans le registre AMR via l'outil `create_mandate`.
4. Vérifier la présence dans la chaîne avec `audit_mandate_chain`.
5. Configurer l'agent pour qu'il appelle `issue_action_token` avant toute action sensible. Côté runtime AMR, le tool `issue_action_token` n'émettra un JWS Ed25519 que si un mandat actif autorise l'action dans son scope. Voir `docs/token-issuance-spec.md` pour le détail.

## Étape 6 — Tests de bout en bout

Avant la mise en production réelle :

- **Test de périmètre** : tenter une action listée dans `excluded_processes`, vérifier le refus d'émission de token et l'événement `refus_emission_token_action` dans le journal.
- **Test human-only** : tenter une action listée dans `restrictions.human_only_mandatory` (ex : `couper_alimentation_baie_production`), vérifier le refus systématique et l'alerte vers l'astreinte.
- **Test de volume** : simuler un pic au-delà de `max_volume_per_day`, vérifier le blocage et le déclenchement du trigger `depassement_volume_quotidien`.
- **Test de supervision SEV-1** : simuler une alerte qualifiée SEV-1 par l'agent, vérifier que la validation humaine est obligatoire avant ouverture de ticket.
- **Test de change** : exécuter un change préapprouvé en lab, vérifier la trace complète dans le journal d'audit (référence CAB, fenêtre de maintenance, ressource cible).
- **Test de révocation immédiate** : révoquer le mandat (déclencheur `incident_de_securite_confirme`), vérifier que l'agent cesse immédiatement d'agir et que toute tentative d'`issue_action_token` est refusée.
- **Test d'audit** : exporter les journaux sur une période courte, vérifier l'intégrité SHA-256.

## Étape 7 — Checklist de validation avant mise en prod

- [ ] Mandat relu et signé par le représentant habilité (DirOps, RSSI ou les deux).
- [ ] RSSI consulté, analyse de risque mise à jour dans le SMSI.
- [ ] CAB consulté si exécution de changes préapprouvés.
- [ ] Notification ANSSI vérifiée si nécessaire au titre de NIS2.
- [ ] Notice clients hébergés mise à jour si applicable.
- [ ] Formation des opérateurs NOC et SRE effectuée et tracée.
- [ ] Registre des activités de traitement RGPD mis à jour.
- [ ] Contrat de sous-traitance signé avec le fournisseur du modèle.
- [ ] Procédure d'escalade et de prise en main humaine documentée et testée.
- [ ] Tests de bout en bout passés.
- [ ] Date de revue du mandat calée (3 à 6 mois selon profil).
- [ ] Plan de continuité ISO 22301 mis à jour avec scénario « agent indisponible ».

## Points d'attention critiques

- **La supervision humaine doit être effective**, pas symbolique. Un opérateur d'astreinte qui valide en masse les qualifications de l'agent sans relire ne remplit pas l'obligation de l'article 14 de l'AI Act.
- **Toute mise à jour majeure du modèle LLM** doit déclencher la révocation du mandat en cours et la signature d'un nouveau mandat. Un modèle n'est pas une variable libre.
- **Les actions human-only mandatory** sont absolues. Le runtime AMR refuse l'émission de token même si le mandat est actif. Un opérateur qui contourne cette règle est en violation du mandat et engage sa responsabilité personnelle.
- **Les transferts de journaux hors UE** sont interdits par défaut. Si le fournisseur du modèle les nécessite, encadrement par clauses contractuelles types et analyse de transfert spécifique.
- **La chaîne d'audit est inutile si personne ne la lit.** Prévoir une revue périodique par l'audit interne, a minima trimestrielle, et un export systématique vers le SOC.
- **Un incident SEV-1 imputable à une action d'agent** déclenche à la fois la révocation du mandat (`incident_sev1_imputable_a_l_agent`) et les obligations de notification AI Act et NIS2. Documenter la procédure unifiée.
