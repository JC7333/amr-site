# Template AMR — Agent Support Client

Template de mandat prêt à l'emploi pour encadrer un agent IA déployé en support client (traitement de tickets entrants, réponse de premier niveau, escalade, remboursement de faible montant, mise à jour de données non sensibles).

## Pour qui

- Directions de la relation client d'ETI et grands comptes qui testent un agent conversationnel en production.
- Responsables conformité et DPO qui doivent cadrer un déploiement déjà en cours sur Zendesk, Intercom, Salesforce Service Cloud ou équivalent.
- Éditeurs et intégrateurs qui proposent un agent à leurs clients et doivent livrer une gouvernance traçable avec le runtime.

## Contexte

Un agent de support client est rarement classé « à haut risque » au sens de l'AI Act — il ne décide pas d'un emploi, d'un crédit ni d'un droit social. Mais il touche à des données personnelles à grande échelle, à des engagements contractuels (remboursements, avoirs, modifications d'abonnement) et à l'image de l'entreprise.

Deux régimes se superposent :

- L'**article 50 du Règlement (UE) 2024/1689** impose d'informer la personne qu'elle interagit avec un système d'IA, sauf si c'est manifeste par le contexte. La date d'application est fixée au **2 août 2026** (article 113).
- Le **Règlement (UE) 2016/679 (RGPD)** encadre le traitement des données du client, sa durée de conservation, et l'obligation d'information (articles 12 à 14).
- Le **Code de la consommation** français encadre les pratiques commerciales : une promesse faite par l'agent (remboursement, délai, geste commercial) engage juridiquement l'entreprise au titre de l'article L.121-1 et suivants.

Déployer un agent de support sans mandat explicite, c'est laisser la machine prendre des engagements commerciaux sans borne chiffrée, sans journal opposable, et sans point d'arrêt en cas de dérive.

## Trois exemples de déploiement concret

1. **Premier niveau conversationnel** : l'agent reçoit les tickets entrants (chat, email), qualifie la demande, répond aux questions de FAQ, et escalade vers un humain tout ce qui sort de son périmètre. Aucun engagement chiffré n'est pris sans validation.
2. **Gestes commerciaux bornés** : l'agent peut proposer un avoir ou un remboursement en dessous d'un seuil (par exemple 30 €), après vérification de l'historique client. Au-delà, escalade obligatoire.
3. **Mise à jour de données non sensibles** : l'agent met à jour une adresse de livraison, un numéro de téléphone ou une préférence de communication, à la demande explicite et tracée du client authentifié. Les données bancaires et l'email principal sont exclus.

## Ce que ce template fournit

- `mandate.yaml` : le mandat structuré prêt à charger dans un registre AMR, avec périmètre d'action, plafonds financiers, restrictions explicites, seuils d'escalade, durée de validité, cartographie RGPD et AI Act article 50.
- `examples/` : trois variantes (permissive, restrictive, équilibrée) commentées, pour s'adapter à la maturité et au niveau de risque de l'organisation.
- `compliance/` : trois fiches courtes qui cartographient le mandat avec l'AI Act (article 50 transparence), le RGPD (information, minimisation, conservation) et le Code de la consommation français.
- `deploy_guide.md` : checklist de mise en production et points d'attention sur l'intégration avec un outil de ticketing.

## Pourquoi c'est risqué sans mandat

Un agent de support client sans mandat documenté expose l'organisation à plusieurs risques concrets :

- **Engagement commercial non borné** : une promesse hallucinée (« votre commande sera remboursée en totalité ») peut être opposée à l'entreprise au titre de l'article 1103 du Code civil et des articles L.121-1 et suivants du Code de la consommation.
- **Sanctions RGPD** : jusqu'à **20 M€ ou 4 %** du chiffre d'affaires mondial en cas de défaut d'information (articles 12, 13) ou de conservation excessive (article 5(1)(e) et article 83).
- **Sanctions AI Act article 50** : jusqu'à **15 M€ ou 3 %** du chiffre d'affaires mondial pour défaut d'information sur l'interaction avec une IA (article 99, paragraphe 4).
- **Dérive réputationnelle** : un échange public viral d'un agent promettant n'importe quoi coûte plus cher, sur la durée, qu'une amende.

Le mandat AMR ne supprime pas ces risques — il les **borne** (plafonds chiffrés) et les **documente** (journal opposable).

## Positionnement tarifaire indicatif

Template vendu en pack clé en main, entre **2 000 € et 5 000 €** selon le niveau d'adaptation :

- **Pack standard (2 000 €)** : les fichiers tels quels, licence d'usage interne, une heure d'accompagnement à la configuration.
- **Pack adapté (3 500 €)** : personnalisation aux conditions générales de vente, aux tarifs de l'entreprise et à l'outil de ticketing en place.
- **Pack intégré (5 000 €)** : déploiement dans un runtime AMR Tier 1, connexion à l'outil ticket, première revue de conformité.

Le template seul ne remplace pas le runtime mandate-gated (Tier 1 AMR, 350 €/mois) ni une validation par un juriste interne. Il pose la structure ; la décision d'engager l'entreprise reste humaine au-delà des seuils.

## À valider côté client avant déploiement

- Revue du mandat par le DPO et le service juridique.
- Mise à jour de la notice d'information client (RGPD, article 13) indiquant l'usage d'un agent IA (AI Act, article 50).
- Ajustement des plafonds financiers aux conditions générales de vente et aux délégations de signature internes.
- Formation des agents humains de niveau 2 aux cas d'escalade.
