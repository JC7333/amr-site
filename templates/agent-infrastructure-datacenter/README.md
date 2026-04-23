# Template AMR — Agent Infrastructure & Datacenter

Template de mandat prêt à l'emploi pour encadrer un agent IA déployé sur une infrastructure d'hébergement, de colocation, d'interconnexion ou de calcul edge (orchestration de configuration, monitoring d'alertes, gestion d'accès, ouverture de tickets, lecture de journaux).

## Pour qui

- Directeurs des opérations et responsables datacenter qui testent un agent IA en assistance NOC ou SOC.
- Responsables sécurité (RSSI) et compliance officers qui doivent encadrer un déploiement déjà en cours.
- Équipes plateforme et SRE qui veulent un mandat lisible par leur outillage et opposable en cas d'incident.
- Intégrateurs et fournisseurs de services managés (MSP) qui livrent un agent à leurs clients hébergeurs.

## Contexte

L'infrastructure de datacenter est une infrastructure critique. Un agent qui touche à la configuration réseau, aux accès physiques, aux journaux d'incident ou à l'orchestration de capacité opère sur des systèmes dont une défaillance produit des effets en cascade (clients hébergés, opérateurs interconnectés, services dépendants).

Plusieurs cadres se superposent :

- Le **Règlement (UE) 2024/1689** dit « AI Act » impose des obligations renforcées dès lors qu'un système d'IA est utilisé dans un contexte de gestion d'infrastructures critiques (Annexe III, point 2). La supervision humaine effective (article 14) et les obligations du déployeur (article 26) s'appliquent pleinement.
- La **Directive (UE) 2022/2555** dite « NIS2 », transposée en droit français par la loi n° 2024-364 du 22 avril 2024, impose des obligations de gestion du risque et de notification d'incident aux opérateurs essentiels et importants, ce qui couvre la majorité des hébergeurs et opérateurs d'interconnexion.
- Les standards **ISO/IEC 27001** (sécurité de l'information), **ISO 22301** (continuité d'activité) et **TIA-942** (infrastructure de datacenter) cadrent les bonnes pratiques opérationnelles.

Déployer un agent sur une infrastructure de production sans mandat explicite, c'est laisser à la machine la possibilité de toucher à la chaîne de production sans borne juridique claire, sans piste d'audit opposable au régulateur, et sans point d'arrêt vérifiable.

## Trois exemples de déploiement concret

1. **Assistance NOC niveau 1** : l'agent reçoit les alertes de monitoring (Prometheus, Zabbix, propriétaires), corrèle avec les dashboards, propose une qualification SEV-2 ou SEV-3, ouvre le ticket dans l'outil de ticketing. Aucune action corrective n'est exécutée par l'agent ; l'opérateur humain valide et déclenche.
2. **Génération de rapports SLA et capacity planning** : l'agent agrège les compteurs d'uptime, de latence, de consommation énergétique et produit un rapport mensuel structuré. Lecture seule sur les métriques agrégées, aucun accès aux données client hébergées.
3. **Orchestration de change management approuvé** : l'agent applique des changements préalablement validés par un comité de change (CAB), uniquement sur des fenêtres de maintenance déclarées, uniquement sur des équipements non critiques (lab, staging, équipements hors production). Tout déploiement en production reste piloté par un opérateur humain habilité.

## Ce que ce template fournit

- `mandate.yaml` : le mandat structuré prêt à charger dans un registre AMR, avec périmètre d'action, volumes maximum, restrictions explicites, seuils de supervision humaine, durée de validité, cartographie AI Act, NIS2 et standards ISO.
- `examples/` : trois variantes (permissive, restrictive, équilibrée) commentées, pour s'adapter au niveau de criticité du site et à la maturité opérationnelle.
- `compliance/` : trois fiches courtes qui cartographient le mandat avec l'AI Act, le RGPD et les règles sectorielles infrastructure (NIS2, ISO 27001, ISO 22301, TIA-942).
- `deploy_guide.md` : checklist de mise en production et points d'attention critiques.

## Lien avec le pivot enforcement AMR

Ce template fournit la configuration de mandat que le tool MCP `issue_action_token` utilisera pour émettre les jetons d'action signés en Ed25519 lors du runtime. Le mandat décrit ce qui est autorisé ; le runtime AMR n'émet un token que si le mandat est actif et couvre l'action demandée dans son scope. Pas de mandat valide, pas de token, pas d'action possible.

La spécification d'émission est documentée dans `docs/token-issuance-spec.md` du registre AMR.

## Pourquoi c'est risqué sans mandat

Un agent qui agit sur une infrastructure critique sans mandat documenté expose l'organisation à plusieurs risques concrets :

- **Sanctions AI Act** : jusqu'à 35 M€ ou 7 % du chiffre d'affaires mondial pour les manquements les plus graves (article 99). Jusqu'à 15 M€ ou 3 % pour les manquements aux obligations sur systèmes à haut risque.
- **Sanctions NIS2** : pour les entités essentielles, amendes administratives jusqu'à 10 M€ ou 2 % du chiffre d'affaires mondial (Directive (UE) 2022/2555, article 34). Pour les entités importantes, jusqu'à 7 M€ ou 1,4 %.
- **Responsabilité civile et contractuelle** : un incident SEV-1 imputable à une action d'agent non encadrée engage la responsabilité du fournisseur vis-à-vis de ses clients hébergés, indépendamment des sanctions réglementaires.
- **Atteinte à la certification** : une certification ISO 27001 ou un agrément sectoriel peut être suspendu si la gouvernance de l'IA opérationnelle n'est pas démontrable.

Le mandat AMR ne supprime pas ces risques — il les **encadre**, les **documente** et les **rend opposables**.

## Positionnement tarifaire indicatif

Template vendu en pack clé en main, entre **3 000 € et 5 000 €** selon le niveau d'adaptation :

- **Pack standard (3 000 €)** : les fichiers tels quels, licence d'usage interne, une heure d'accompagnement à la configuration.
- **Pack adapté (4 000 €)** : personnalisation du mandat aux outils internes (ticketing, monitoring, gestionnaire de configuration) et aux procédures change management de l'organisation.
- **Pack intégré (5 000 €)** : déploiement dans un runtime AMR Tier 1, connexion aux systèmes de monitoring et de ticketing, première revue de conformité avec le RSSI.

Le template seul ne remplace pas le runtime mandate-gated (Tier 1 AMR, 350 €/mois) ni une revue par un RSSI. Il pose la structure ; la décision d'autoriser un agent à toucher à l'infrastructure reste humaine.

## À valider côté client avant déploiement

- Revue du mandat par le RSSI et le responsable des opérations.
- Cartographie des actifs touchés et de leur criticité (lien avec le SMSI ISO 27001).
- Validation par le comité change management (CAB) si l'agent est habilité à exécuter des changements approuvés.
- Mise à jour du registre des traitements RGPD si des données personnelles transitent dans les journaux exploités par l'agent.
- Notification préalable à l'autorité compétente si requise par la transposition NIS2 (en France : ANSSI).
