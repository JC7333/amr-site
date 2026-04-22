# Cartographie AI Act — Agent Marketing & Contenu

Référence : **Règlement (UE) 2024/1689** du Parlement européen et du Conseil établissant des règles harmonisées concernant l'intelligence artificielle.

## Classification

Un agent de production de contenu marketing n'est pas, en règle générale, listé à l'**Annexe III** du Règlement. Il ne décide ni d'un emploi, ni d'un crédit, ni d'un droit social. À ce titre, il ne relève **pas** du régime des systèmes à haut risque du Chapitre III, Section 2.

Il relève en revanche de l'**article 50 du Règlement**, qui impose des obligations de transparence et, pour certains contenus, de marquage.

## Obligation principale — Article 50, paragraphe 1 (interaction)

> Article 50, paragraphe 1 : « Les fournisseurs veillent à ce que les systèmes d'IA destinés à interagir directement avec des personnes physiques soient conçus et développés de manière à ce que les personnes physiques concernées soient informées qu'elles interagissent avec un système d'IA, sauf si cela est évident pour une personne physique raisonnablement bien informée, attentive et avisée. »

Dans le template : section `agent.user_disclosure`, champs `disclosure_text_fr` et `disclosure_channels`. Couvre les cas chatbot site public, formulaire intelligent, assistant éditorial externe.

## Obligation centrale — Article 50, paragraphe 4 (marquage des contenus)

> Article 50, paragraphe 4 : « Les déployeurs d'un système d'IA qui génère ou manipule des images ou des contenus audio ou vidéo constituant un hypertruquage indiquent que les contenus ont été générés ou manipulés par une IA. […] Les déployeurs d'un système d'IA qui génère ou manipule des textes publiés dans le but d'informer le public sur des questions d'intérêt public indiquent que le texte a été généré ou manipulé par une IA. »

Dans le template : section `agent.output_marking` qui exige un marquage machine-readable (C2PA ou équivalent) sur tout contenu généré ou substantiellement modifié, et une mention humaine visible quand le contexte éditorial l'exige.

**Limites de l'obligation textuelle** : l'obligation de mention visible ne s'applique pas systématiquement au contenu purement promotionnel et publicitaire de l'entreprise sur ses propres canaux ; elle vise les contenus « informant le public sur des questions d'intérêt public ». Le gabarit retient une lecture prudente : marquage technique systématique, mention humaine adaptée au contexte. **À VALIDER PAR JURISTE** au cas par cas.

## Obligation du déployeur — Article 26

L'article 26 impose au déployeur d'un système d'IA :

- Utiliser le système conformément à la notice (paragraphe 1).
- Confier la supervision humaine à des personnes formées (paragraphe 2).
- Tenir à jour les journaux générés automatiquement, dans la limite du contrôle du déployeur (paragraphe 6).

Dans le template : la responsabilité du déployeur est matérialisée par `principal.representative`, `human_oversight.reviewer_profile`, `audit_trail`.

## Obligation complémentaire — Article 14 (principe général)

Bien que non formellement obligatoire hors haut risque, le principe de supervision humaine de l'article 14 est transposé par la règle `human_oversight.mandatory_validation_before_publication: true`. Aucun contenu ne quitte l'environnement de l'agent sans décision humaine de publication.

## Calendrier d'application

Les obligations de l'article 50 s'appliquent à partir du **2 août 2026**, conformément à l'article 113 du Règlement. Cette date n'est pas concernée, à ce stade, par les discussions de report en cours sur le paquet dit « Digital Omnibus », qui portent principalement sur les systèmes à haut risque de l'Annexe III. **À suivre au regard des trilogues.**

## Sanctions encourues

Article 99, paragraphe 4 : jusqu'à **15 M€ ou 3 % du chiffre d'affaires mondial annuel**, le montant le plus élevé étant retenu, pour les manquements aux obligations applicables aux fournisseurs ou aux déployeurs, y compris l'article 50.

## Rôle du déployeur vs fournisseur

L'article 50 impose des obligations à la fois au **fournisseur** du système (celui qui conçoit le modèle et le met sur le marché) et au **déployeur** (l'entreprise qui exploite l'agent). Pour le marquage des contenus (article 50, paragraphe 4), l'obligation pèse expressément sur le **déployeur**.

Le déployeur reste également responsable au titre de l'article 26 :
- s'assurer que la notice de transparence est affichée sur les canaux conversationnels publics ;
- s'assurer que le marquage des contenus est correctement appliqué dans la chaîne de publication ;
- former les équipes humaines aux cas d'escalade ;
- tenir à jour les journaux de fonctionnement.

## Points à valider par un juriste

- Confirmer l'absence de bascule en Annexe III pour les cas d'usage périphériques. Exemple : si l'agent participe à du *lead scoring* qui décide d'une éligibilité commerciale produisant un effet juridique, l'article 22 du RGPD et possiblement l'Annexe III peuvent être déclenchés. **À VALIDER PAR JURISTE.**
- Confirmer l'étendue exacte de l'obligation de mention visible de l'article 50, paragraphe 4 selon la nature du contenu (publicitaire, éditorial, journalistique, intérêt public).
- Vérifier l'articulation avec le **Règlement (UE) 2022/2065 (DSA)** si l'organisation est qualifiée de plateforme intermédiaire ou si elle place des annonces ciblées.
- Vérifier l'articulation avec les recommandations du **Conseil supérieur de l'audiovisuel et du numérique (Arcom)** si du contenu audiovisuel est généré.
