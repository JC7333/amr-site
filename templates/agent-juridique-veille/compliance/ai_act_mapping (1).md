# Cartographie AI Act — Agent Juridique & Veille

Référence : **Règlement (UE) 2024/1689** du Parlement européen et du Conseil établissant des règles harmonisées concernant l'intelligence artificielle.

## Classification

Un agent de veille juridique pure n'est, en règle générale, **pas** classé à haut risque au sens de l'**Annexe III** du Règlement. Il ne décide ni d'un emploi, ni d'un crédit, ni d'un droit social, ni d'une prestation essentielle pour une personne identifiée. Il consomme des informations publiques et produit des synthèses qui restent qualifiées par un juriste humain.

Il relève en revanche de l'**article 50** du Règlement, qui impose des obligations de transparence dès lors que le système d'IA interagit directement avec des personnes physiques (par exemple un chatbot interne à un service juridique, ou un assistant accessible aux juristes du cabinet).

**Cas de bascule en haut risque (Annexe III) à surveiller** :

- Si l'agent participe à une aide à la décision dans un processus d'**emploi**, de **gestion des travailleurs** ou d'**accès à l'emploi indépendant** (Annexe III point 4) — par exemple, en alimentant une recommandation de licenciement à partir d'une jurisprudence prud'homale.
- Si l'agent contribue à l'**administration de la justice** (Annexe III point 8) en assistant directement un magistrat ou en alimentant une décision juridictionnelle.
- Si l'agent évalue l'**éligibilité à des prestations essentielles** privées (point 5) à partir de critères juridiques.

Dans ces cas, l'ensemble des obligations du Chapitre III, Section 2 du Règlement s'appliquent, ce qui change radicalement le cadre du déploiement.

**À VALIDER PAR JURISTE** : la frontière entre veille pure et aide à la décision est parfois ténue. Tout déploiement où l'agent produit des recommandations à fort impact opérationnel doit être qualifié au cas par cas.

## Obligations mappées dans `mandate.yaml`

### Article 12 — Tenue de registres

Le système doit enregistrer automatiquement les événements pertinents pendant toute sa durée de vie.

Dans le template : section `audit_trail.logged_events` couvrant la création de mandat, la consultation de sources, la génération de synthèses, les déclenchements de revue humaine, les escalades. La chaîne SHA-256 (`tamper_evidence: sha256_chain`) garantit l'intégrité des traces.

### Article 13 — Transparence vis-à-vis du déployeur

Le système doit fournir au déployeur des informations claires sur son fonctionnement.

Dans le template : section `agent.purpose` et `compliance_mapping`. La notice d'information aux utilisateurs internes (juristes, avocats collaborateurs) reste à la charge du déployeur, en s'appuyant sur le texte fourni dans `agent.user_disclosure.disclosure_text_fr`.

### Article 14 — Supervision humaine (principe général)

Bien que l'agent ne soit pas formellement classé à haut risque, le principe de supervision humaine de l'article 14 est transposé par la règle `human_oversight.mandatory_validation_before_publication: true`. Aucune publication interne ne quitte l'environnement de l'agent sans validation humaine. Trois régimes possibles sont proposés selon les variantes : `human_in_the_loop_strict` (toute sortie validée), `human_in_the_loop` (validations sur seuils), `human_on_the_loop` (validation par échantillon ou sur déclencheurs).

### Article 26 — Obligations du déployeur

L'article 26 impose au déployeur :

- Utiliser le système conformément à la notice du fournisseur (paragraphe 1).
- Confier la supervision humaine à des personnes formées (paragraphe 2).
- Tenir à jour les journaux automatiques générés (paragraphe 6).

Dans le template : la responsabilité du déployeur est matérialisée par `principal.representative`, `human_oversight.reviewer_profile` (juriste diplômé ou avocat inscrit), `audit_trail`. Le profil du reviewer est explicitement contraint à des personnes habilitées juridiquement.

### Article 50 — Transparence (interaction avec personnes)

> Article 50, paragraphe 1 : « Les fournisseurs veillent à ce que les systèmes d'IA destinés à interagir directement avec des personnes physiques soient conçus et développés de manière à ce que les personnes physiques concernées soient informées qu'elles interagissent avec un système d'IA, sauf si cela est évident pour une personne physique raisonnablement bien informée, attentive et avisée. »

Dans le template : section `agent.user_disclosure` qui documente la notice à afficher dès qu'un juriste interne dialogue avec l'agent ou reçoit une fiche produite par l'agent. L'événement d'affichage est journalisé.

### Article 50 paragraphe 4 — Marquage des contenus textuels

Si l'agent produit des textes diffusés à des fins d'information publique (par exemple, une newsletter de cabinet adressée à des clients ou prospects), un marquage humain visible peut être requis selon la lecture du paragraphe 4. **À VALIDER PAR JURISTE** au cas par cas.

## Calendrier d'application

Les obligations relatives aux systèmes à haut risque de l'Annexe III s'appliquent à partir du **2 août 2026**, conformément à l'article 113 du Règlement. Les obligations de l'article 50 s'appliquent à la même date.

Un report partiel via le paquet dit « Digital Omnibus » est en discussion au niveau européen au moment de la rédaction de ce template. Selon le compromis envisagé, certaines obligations sur les systèmes à haut risque de l'Annexe III pourraient être repoussées au **2 décembre 2027**. Les trilogues ne sont pas conclus à la date de rédaction. **À suivre.**

Le mandat reste valable dans les deux scénarios.

## Sanctions encourues

Article 99 du Règlement :

- Jusqu'à **35 M€ ou 7 % du chiffre d'affaires mondial annuel** pour les manquements les plus graves (pratiques interdites, article 5).
- Jusqu'à **15 M€ ou 3 %** pour les manquements aux obligations des systèmes à haut risque, ou aux obligations applicables aux fournisseurs et déployeurs, y compris l'article 50.

## Points à valider par un juriste

- Vérifier que le déploiement prévu ne bascule pas en Annexe III par un effet de bord (lien avec décision RH, scoring de personnes, aide à la décision judiciaire). **À VALIDER PAR JURISTE.**
- Confirmer la qualité de « déployeur » au sens du Règlement (articles 3 et 25) et la répartition des responsabilités avec le fournisseur du modèle.
- Vérifier l'articulation avec le **Règlement (UE) 2022/2065 (Digital Services Act)** si l'organisation est qualifiée de plateforme intermédiaire.
- S'assurer que l'évaluation de conformité et le marquage CE du système fourni ont bien été réalisés en amont par le fournisseur du modèle, lorsque cela s'applique.
