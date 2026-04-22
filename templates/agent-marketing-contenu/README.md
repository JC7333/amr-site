# Template AMR — Agent Marketing & Contenu

Template de mandat prêt à l'emploi pour encadrer un agent IA déployé en production marketing : génération de contenus éditoriaux, posts réseaux sociaux, séquences email, briefs créatifs, optimisation SEO, recyclage d'assets existants.

## Pour qui

- Directions marketing et communication d'ETI et de grands comptes qui industrialisent la production de contenu avec un agent.
- Agences et éditeurs qui livrent un agent à leurs clients et doivent fournir une gouvernance documentée à côté du runtime.
- Responsables conformité, DPO et juristes propriété intellectuelle qui doivent cadrer un déploiement déjà en cours sur des outils type HubSpot, Marketo, Salesforce Marketing Cloud, ou des stacks internes.

## Contexte réglementaire

Un agent de production de contenu marketing n'est pas, en règle générale, classé « à haut risque » au sens de l'**Annexe III du Règlement (UE) 2024/1689** (AI Act). Il relève en revanche de plusieurs régimes superposés :

- L'**article 50 du Règlement (UE) 2024/1689** impose, lorsque l'agent interagit directement avec des personnes physiques (chatbot conversationnel, assistant éditorial public), d'informer la personne qu'elle interagit avec une IA. L'article 50 paragraphe 4 impose en outre, pour les contenus dits « hypertruquages » (deepfakes) et les textes publiés à des fins d'information du public, une obligation de marquage.
- Le **Règlement (UE) 2016/679 (RGPD)** s'applique dès lors que l'agent traite des données personnelles (segmentation, personnalisation, scoring marketing, A/B testing nominatif).
- Le **Code de la propriété intellectuelle** français encadre la réutilisation d'œuvres protégées dans les sorties de l'agent (articles L.122-4 et L.122-5).
- Le **Code de la consommation** sanctionne les pratiques commerciales trompeuses (articles L.121-1 à L.121-5).
- Le **Règlement (UE) 2022/2065 (Digital Services Act)** crée des obligations de transparence sur la publicité en ligne pour les plateformes intermédiaires.

Déployer un agent marketing sans mandat documenté, c'est laisser la machine produire des claims commerciaux, citer des sources, réutiliser des marques tierces et adresser des audiences segmentées sans borne, sans journal opposable et sans point d'arrêt.

## Trois exemples de déploiement concret

1. **Génération de posts réseaux sociaux** : l'agent reçoit un brief court, produit trois variantes pour LinkedIn, Instagram et X, et propose un calendrier. Aucune publication directe : un humain valide chaque sortie avant programmation.
2. **Optimisation SEO de pages existantes** : l'agent analyse une page, propose une réécriture optimisée pour un mot-clé cible, suggère des balises et un maillage interne. La publication reste manuelle.
3. **Personnalisation de séquences email** : l'agent adapte un email-mère à 5 segments d'audience (volume autorisé borné), sans accès aux noms ni adresses, à partir de variables anonymisées. Envoi par l'outil de marketing automation après validation.

## Ce que ce template fournit

- `mandate.yaml` : le mandat structuré prêt à charger dans un registre AMR, avec périmètre éditorial, plafonds de publication, restrictions sur la propriété intellectuelle, seuils d'escalade humaine, durée de validité, cartographie RGPD et AI Act.
- `examples/` : trois variantes (permissive, restrictive, équilibrée) commentées, pour s'adapter à la maturité éditoriale et au niveau de risque de marque.
- `compliance/` : trois fiches courtes qui cartographient le mandat avec l'AI Act (articles 50, 26), le RGPD (information, profilage, prospection) et les règles sectorielles (propriété intellectuelle, publicité, secteurs régulés).
- `deploy_guide.md` : checklist de mise en production et points d'attention sur l'intégration avec un outil de marketing automation ou un CMS.

## Pourquoi c'est risqué sans mandat

Un agent marketing sans mandat documenté expose l'organisation à plusieurs risques concrets :

- **Atteinte aux droits de tiers** : la reproduction non autorisée d'une œuvre protégée est sanctionnée jusqu'à **300 000 € et 3 ans d'emprisonnement** (Code de la propriété intellectuelle, article L.335-2).
- **Pratiques commerciales trompeuses** : un claim faux sur les caractéristiques d'un produit est sanctionné jusqu'à **300 000 €** pour une personne physique, **1,5 M€** pour une personne morale, et la peine peut être portée à **10 % du chiffre d'affaires moyen annuel** (Code de la consommation, article L.132-2).
- **Sanctions RGPD** : jusqu'à **20 M€ ou 4 % du chiffre d'affaires mondial** en cas de profilage illicite ou de prospection sans base légale (articles 6, 21, 22, 83).
- **Sanctions AI Act article 50** : jusqu'à **15 M€ ou 3 % du chiffre d'affaires mondial** pour défaut d'information sur l'interaction avec une IA ou défaut de marquage des contenus générés (article 99, paragraphe 4).
- **Risque de marque** : un message hors charte, un visuel généré inapproprié ou une prise de position non autorisée coûte plus cher en réputation qu'en amende.

Le mandat AMR ne supprime pas ces risques — il les **borne** (volumes, plafonds, listes de marques interdites) et les **documente** (journal opposable, traçabilité éditoriale).

## Positionnement tarifaire indicatif

Template vendu en pack clé en main, entre **2 000 € et 5 000 €** selon le niveau d'adaptation :

- **Pack standard (2 000 €)** : les fichiers tels quels, licence d'usage interne, une heure d'accompagnement à la configuration.
- **Pack adapté (3 500 €)** : personnalisation à la charte éditoriale, à la liste de marques tierces interdites et à l'outil de marketing automation en place.
- **Pack intégré (5 000 €)** : déploiement dans un runtime AMR Tier 1, connexion à l'outil marketing, première revue de conformité par un juriste partenaire.

Le template seul ne remplace pas le runtime mandate-gated (Tier 1 AMR, 350 €/mois) ni une validation par un juriste interne. Il pose la structure ; la décision de publier reste humaine au-delà des seuils.

## À valider côté client avant déploiement

- Revue du mandat par la direction marketing, le service juridique et le DPO.
- Mise à jour de la notice d'information client (RGPD, article 13) si une personnalisation nominative est activée.
- Intégration de la mention article 50 de l'AI Act sur les canaux conversationnels publics (chatbot, formulaire intelligent).
- Validation de la liste des marques, personnalités et œuvres exclues du périmètre.
- Formation des équipes éditoriales aux cas d'escalade et au refus de publication.
