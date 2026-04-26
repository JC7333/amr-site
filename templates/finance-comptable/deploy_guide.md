# Guide de déploiement — Template AMR Agent Finance & Comptable

Ce guide accompagne la mise en production d'un agent IA dans la chaîne crédit, comptable ou LCB-FT en utilisant ce template de mandat AMR. Il est destiné au compliance officer, au directeur financier et au responsable LCB-FT qui pilotent le déploiement.

## Avant le déploiement — checklist de validation

### Documentation réglementaire à constituer

- [ ] DPIA réalisée et signée (obligatoire pour scoring crédit, fortement recommandée sinon)
- [ ] Test de mise en balance documenté si la base légale RGPD est l'intérêt légitime
- [ ] Inscription du traitement au registre des activités de traitement (article 30 RGPD)
- [ ] Mise à jour de la documentation LCB-FT si l'agent intervient en première ligne
- [ ] Notification au responsable conformité DORA si l'entité est dans le périmètre
- [ ] Information du commissaire aux comptes pour les entités sous contrôle externe

### Personnalisation du mandate.yaml

- [ ] Renseigner `principal.legal_name`, `principal.registration.id_value` (SIREN)
- [ ] Renseigner `principal.representative` avec une personne habilitée juridiquement à signer
- [ ] Préciser `principal.sector_status.activity_type` (établissement de crédit, EME, EP, fintech BNPL, expert-comptable, etc.)
- [ ] Identifier la base légale RGPD adaptée à chaque finalité
- [ ] Renseigner le statut DPIA et la référence interne
- [ ] Renseigner le périmètre DORA et LCB-FT
- [ ] Adapter `scope.business_processes` au périmètre exact de l'agent
- [ ] Calibrer `permissions` avec des plafonds journaliers cohérents avec le volume métier réel
- [ ] Lister explicitement `restrictions.forbidden_actions` et `prohibited_criteria`
- [ ] Calibrer `human_oversight.mandatory_review_triggers` avec des seuils chiffrés
- [ ] Renseigner `expiration.valid_from` et `valid_until` (6 mois maximum recommandés)
- [ ] Lister les `revocation_contacts` joignables 24/7

### Validation interne

- [ ] Revue du mandat par le compliance officer
- [ ] Revue par le DPO sur les volets RGPD et article 22
- [ ] Revue par le responsable LCB-FT si premier ligne LCB-FT dans le scope
- [ ] Revue par le directeur financier sur la cohérence des plafonds métier
- [ ] Validation par la direction générale (le mandat est un acte d'autorisation à effet juridique)

### Capacité de revue humaine

- [ ] L'effectif humain de revue est dimensionné pour les volumes prévus
- [ ] Les opérateurs de revue ont reçu la formation listée dans `human_oversight.reviewer_profile.training_topics`
- [ ] Le canal de contestation pour les personnes concernées est opérationnel et documenté
- [ ] La capacité d'infirmer une proposition de l'agent est démontrée et testée
- [ ] Le temps de revue alloué par dossier permet une intervention humaine **significative**, pas un simple clic

### Intégration technique avec le runtime AMR

- [ ] Le mandate.yaml est chargé dans le registre AMR
- [ ] Le tool MCP `issue_action_token` est connecté au runtime de l'agent
- [ ] La clé publique Ed25519 du registre est distribuée aux consumers (validation offline)
- [ ] La table `issued_tokens` est dimensionnée pour les volumes attendus
- [ ] Les triggers de révocation sont câblés sur les systèmes opérationnels (SIEM, ticketing, alertes LCB-FT)

La spécification d'émission est documentée dans `docs/token-issuance-spec.md` du registre AMR.

## Pendant l'exploitation — points d'attention

- **Surveillance des biais** : un scoring de crédit peut développer un biais systématique non détectable au déploiement initial. Mettre en place une revue mensuelle des taux d'acceptation et de refus par segments (avec attention aux proxies de critères discriminatoires).
- **Surveillance des dépassements de seuils** : les triggers `mandatory_review_triggers` doivent générer des alertes vers le compliance officer. Un dépassement répété signale soit un sous-dimensionnement des seuils, soit une dérive du périmètre.
- **Surveillance des refus de token** : un volume élevé de `refus_emission_token_action` dans les logs indique que l'agent tente des actions hors scope. Investiguer.
- **Mise à jour du modèle LLM** : toute mise à jour majeure du modèle par le fournisseur déclenche une révocation immédiate du mandat (`revocation.immediate_triggers`). Re-tester avant réémission.
- **Revue trimestrielle** : revoir le mandat tous les trois mois minimum, même si la durée de validité est plus longue. Documenter les revues.

## En cas d'incident

- **Incident de sécurité** : révocation immédiate du mandat, notification CNIL si données personnelles touchées (article 33 RGPD, 72 heures), notification ACPR si entité dans périmètre DORA (article 19).
- **Réclamation client sur décision automatisée** : intervention humaine immédiate pour réévaluer le dossier. Documenter la suite donnée. Conserver la trace pendant la durée de prescription (5 ans pour les actions civiles).
- **Biais systématique détecté** : suspension du périmètre concerné, audit du modèle, révocation et réémission après correction.
- **Contrôle ACPR ou CNIL** : produire le mandat, les journaux d'audit, la DPIA et le test de mise en balance. Le mandat AMR sert de pièce documentaire opposable.

## En fin de mandat

- [ ] Renouveler le mandat si la mission de l'agent est reconduite (réémission complète, pas simple prolongation)
- [ ] Conserver l'ancien mandat et ses journaux pendant les durées de conservation applicables (10 ans pour pièces comptables, 5 ans pour LCB-FT et dossiers crédit)
- [ ] Documenter les évolutions entre versions successives du mandat

## Pour aller plus loin

- Spec d'émission de token AMR : `docs/token-issuance-spec.md`
- Cartographies réglementaires : `compliance/ai_act_mapping.md`, `compliance/rgpd_mapping.md`, `compliance/sector_specific.md`
- Variantes de mandat : `examples/permissive.yaml`, `examples/restrictive.yaml`, `examples/balanced.yaml`

Le runtime mandate-gated AMR (Tier 1, 350 €/mois) automatise l'émission et la vérification des tokens d'action en production. Sans runtime, le mandat reste une référence documentaire utile mais n'est pas opposable de manière automatisée à chaque action de l'agent.
