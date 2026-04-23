# Cartographie RGPD — Agent Infrastructure & Datacenter

Référence : **Règlement (UE) 2016/679** (RGPD) et **Loi n° 78-17 du 6 janvier 1978 modifiée** (Loi Informatique et Libertés).

## Données concernées

Un agent d'infrastructure traite principalement des **données opérationnelles** (métriques, journaux système, tickets internes) et non des données personnelles de clients ou d'utilisateurs finaux. Le template proscrit explicitement l'accès au contenu du trafic client (`data_access.client_traffic_content_access: "interdit"`) et au contenu des données hébergées (`data_access.client_data_access: "interdit"`).

Cependant, plusieurs catégories de données personnelles peuvent transiter dans le périmètre :

- **Identifiants des opérateurs et techniciens** (nom, login, identifiant carte d'accès) présents dans les journaux système et de ticketing.
- **Données de connexion** (adresses IP source, journaux d'accès) pouvant identifier des personnes physiques.
- **Données présentes dans les tickets** (signalements clients qui peuvent contenir des éléments nominatifs).

## Base légale — Article 6

Le template retient l'**intérêt légitime** (article 6(1)(f)) comme base légale par défaut pour le traitement des données opérationnelles internes. L'intérêt poursuivi est la supervision et la sécurité de l'infrastructure.

Le recours à l'intérêt légitime suppose la tenue d'un **test de mise en balance** documenté. Pour les données opérationnelles internes (métriques, identifiants techniques anonymisés), l'analyse est généralement favorable. **À VALIDER PAR JURISTE** selon le contexte précis.

Dans le template : section `principal.legal_basis_gdpr` et référence `balancing_test_ref`.

## Article 28 — Sous-traitance

Si l'agent est fourni ou hébergé par un prestataire tiers (cas fréquent : modèle LLM hébergé hors infrastructure de l'opérateur), un **contrat de sous-traitance** au sens de l'article 28 est nécessaire.

Points à couvrir : finalités, instructions documentées, confidentialité, sécurité, sous-traitance ultérieure, assistance, suppression ou restitution, audit. **À VALIDER PAR JURISTE.**

Le template impose `transfer_outside_eu: false` par défaut. Un transfert hors UE déclenche les obligations des articles 44 à 49 (clauses contractuelles types, analyse de transfert, etc.).

## Article 30 — Registre des activités de traitement

Le déploiement d'un agent qui lit des journaux contenant des données personnelles doit être inscrit au registre des activités de traitement.

Le mandat AMR fournit la matière documentaire : finalité (`agent.purpose`), catégories de données (`data_access.categories`), durées de conservation (`data_access.retention`), mesures de sécurité (`audit_trail`, `human_oversight`).

## Article 32 — Sécurité du traitement

Les mesures techniques et organisationnelles appropriées incluent typiquement :

- **Anonymisation** des journaux système avant exposition à l'agent (`anonymisation_required: true`).
- **Chiffrement** des journaux d'audit AMR au repos et en transit.
- **Contrôle d'accès** strict aux journaux d'audit (`audit_trail.log_access` limité).
- **Tests de résilience** réguliers (cohérence avec ISO 22301).

## Article 33 — Notification de violation

Une violation de données personnelles imputable à une action d'agent doit être notifiée à la CNIL dans les **72 heures** lorsqu'elle représente un risque pour les droits et libertés des personnes.

Le journal d'audit AMR (avec sa chaîne SHA-256 inviolable) facilite la qualification rapide et la documentation de la notification.

## Articulation avec NIS2 sur la notification d'incident

Un incident de sécurité touchant à la fois la confidentialité de données personnelles et la disponibilité d'un service essentiel peut déclencher **simultanément** :

- une notification CNIL au titre de l'article 33 RGPD (72 heures) ;
- une notification ANSSI au titre de l'article 23 NIS2 (24 heures pour l'alerte précoce).

Les deux notifications sont indépendantes et cumulatives.

## Décision automatisée — Article 22

L'article 22 interdit, sauf exceptions, la décision produisant des effets juridiques ou affectant significativement la personne lorsqu'elle est fondée exclusivement sur un traitement automatisé.

Pour un agent d'infrastructure, la question peut se poser pour :

- une **suspension de service client** déclenchée par l'agent (effets contractuels) — proscrite par le template (`forbidden_actions: supprimer_donnees_client`, et le routage de toute action vers un humain pour les SEV-1).
- une **modification d'accès d'un technicien** déclenchée par l'agent (effets sur la relation de travail) — encadrée par `requires_human_approval: true` sur les demandes d'accès physique.

Dans le template : aucune action affectant directement une personne identifiée n'est autorisée sans validation humaine effective.

## Points à valider par un DPO

- Test de mise en balance pour l'intérêt légitime (article 6(1)(f)).
- Cartographie précise des données personnelles transitant dans les journaux exploités par l'agent.
- Mise à jour du registre des activités de traitement (article 30).
- Contrat de sous-traitance avec le fournisseur du modèle (article 28), en particulier sur les transferts hors UE.
- Information des techniciens et opérateurs dont l'activité est tracée par les journaux exploités par l'agent.
- Articulation des procédures de notification d'incident (CNIL article 33, ANSSI article 23 NIS2).
