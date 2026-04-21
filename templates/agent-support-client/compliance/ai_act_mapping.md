# Cartographie AI Act — Agent Support Client

Référence : **Règlement (UE) 2024/1689** du Parlement européen et du Conseil établissant des règles harmonisées concernant l'intelligence artificielle.

## Classification

Un agent conversationnel de support client de premier niveau n'est pas, en règle générale, listé à l'**Annexe III** du Règlement. Il ne décide ni d'un emploi, ni d'un crédit, ni d'un droit social, ni d'une prestation essentielle. À ce titre, il ne relève **pas** du régime des systèmes à haut risque du Chapitre III, Section 2.

Il relève en revanche de l'**article 50 du Règlement**, qui impose des obligations de transparence pour les systèmes d'IA « destinés à interagir directement avec des personnes physiques ».

## Obligation principale — Article 50

> Article 50, paragraphe 1 : « Les fournisseurs veillent à ce que les systèmes d'IA destinés à interagir directement avec des personnes physiques soient conçus et développés de manière à ce que les personnes physiques concernées soient informées qu'elles interagissent avec un système d'IA, sauf si cela est évident pour une personne physique raisonnablement bien informée, attentive et avisée. »

Dans le template : section `agent.user_disclosure`, champ `disclosure_text_fr` et `disclosure_channels`. L'événement d'affichage de la notice est journalisé (`audit_trail.logged_events : disclosure_ai_act_article_50_affichee`).

## Obligation complémentaire — Article 14 (principe général)

Bien que non formellement obligatoire hors haut risque, le principe de supervision humaine de l'article 14 est transposé dans la section `human_oversight` pour deux raisons :

1. Limiter l'engagement commercial de l'entreprise (Code civil, article 1103).
2. Protéger les personnes vulnérables (détresse manifeste, réclamation, exercice des droits RGPD).

Trois régimes possibles sont proposés : `human_in_the_loop` (pilote, chaque réponse validée), `human_on_the_loop` (production, revue par échantillonnage statistique) et des déclencheurs automatiques d'escalade.

## Calendrier d'application

Les obligations de l'article 50 s'appliquent à partir du **2 août 2026**, conformément à l'article 113 du Règlement. Cette date n'est pas concernée par les discussions de report actuellement en cours sur le paquet dit « Digital Omnibus », qui portent principalement sur les systèmes à haut risque de l'Annexe III. **À suivre au regard des trilogues en cours.**

## Sanctions encourues

Article 99, paragraphe 4 : jusqu'à **15 M€ ou 3 % du chiffre d'affaires mondial annuel**, le montant le plus élevé étant retenu, pour les manquements aux obligations applicables aux fournisseurs ou aux déployeurs, y compris l'article 50.

## Rôle du déployeur vs fournisseur

L'article 50 impose l'obligation au **fournisseur** du système (celui qui conçoit et met sur le marché). Toutefois, le **déployeur** (l'entreprise qui exploite l'agent) reste responsable au titre de l'article 26 du Règlement de l'utilisation conforme, notamment :

- S'assurer que la notice de transparence est bien affichée dans son intégration (canal web, email, messagerie instantanée).
- Former les équipes humaines à reprendre la main quand l'agent escalade.
- Tenir à jour les journaux de fonctionnement.

Dans le template : la responsabilité du déployeur est matérialisée par `principal.representative`, `human_oversight.reviewer_profile`, et `audit_trail`.

## Points à valider par un juriste

- Confirmer que le cas d'usage ne bascule pas dans l'Annexe III par un effet de bord (exemple : si l'agent décide d'accorder ou refuser un crédit, il relève de l'Annexe III point 5 ; si l'agent évalue l'éligibilité à une prestation sociale, il relève du point 5.a). **À VALIDER PAR JURISTE.**
- Confirmer la qualité de « déployeur » au sens du Règlement (articles 3 et 25) et la répartition des responsabilités avec le fournisseur du modèle.
- Vérifier que la notice de transparence est bien rendue visible et pas dissimulée dans des conditions générales.
