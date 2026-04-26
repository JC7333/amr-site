# Cartographie RGPD — Template Finance & Comptable

Ce document cartographie le mandat avec le **Règlement (UE) 2016/679** dit « RGPD ». Les traitements financiers et comptables touchent fréquemment à des données personnelles ; le scoring de crédit envers une personne physique relève en plus de l'article 22 sur la décision individuelle automatisée.

## Article 6 — Base légale

La base légale dépend du traitement précis. Le mandat distingue trois cas :

- **Article 6(1)(b) — Exécution du contrat** : applicable lorsque le traitement est nécessaire à l'exécution d'un contrat conclu avec la personne (gestion d'un dossier de financement souscrit, facturation, gestion comptable d'un compte client).
- **Article 6(1)(c) — Obligation légale** : applicable pour les traitements imposés par le Code monétaire et financier (LCB-FT, articles L.561-1 et suivants), le Code de commerce (obligations comptables, article L.123-12) et le droit fiscal.
- **Article 6(1)(f) — Intérêt légitime** : applicable pour le scoring interne et la prévention de la fraude, sous réserve d'un test de mise en balance documenté qui démontre que les intérêts du responsable ne prévalent pas indûment sur les droits de la personne.

**À VALIDER PAR JURISTE** : la base légale doit être identifiée pour chaque finalité et documentée dans le registre des traitements (article 30). Un traitement utilisant simultanément plusieurs bases sans distinction n'est pas conforme.

## Article 9 — Catégories particulières de données

Les données suivantes sont **interdites** dans tout traitement de scoring ou décision automatisée par l'agent :

- Origine raciale ou ethnique
- Opinions politiques
- Convictions religieuses ou philosophiques
- Appartenance syndicale
- Données génétiques
- Données biométriques aux fins d'identifier une personne physique
- Données concernant la santé
- Données concernant la vie sexuelle ou l'orientation sexuelle

Le mandat couvre cette interdiction via `restrictions.prohibited_criteria` et via la liste `data_access.fields_forbidden`. Le runtime AMR refusera l'émission de token si l'agent tente d'accéder à ces champs.

**Attention aux proxies** : un critère facialement neutre peut constituer un proxy discriminatoire (code postal seul, patronyme seul, langue maternelle). Le mandat liste explicitement les proxies à exclure dans `prohibited_criteria`.

## Article 22 — Décision individuelle automatisée

C'est l'article central pour le scoring de crédit. La personne dispose du droit de ne pas faire l'objet d'une décision fondée exclusivement sur un traitement automatisé produisant des effets juridiques la concernant ou l'affectant de manière significative.

Trois exceptions existent (article 22.2) :

- Le traitement est nécessaire à la conclusion ou à l'exécution d'un contrat,
- Le traitement est autorisé par le droit de l'Union ou d'un État membre,
- Le traitement est fondé sur le consentement explicite de la personne.

**Même dans ces cas d'exception**, l'article 22.3 impose la mise en place de mesures appropriées qui doivent inclure au minimum :

- Le droit d'obtenir une **intervention humaine** de la part du responsable du traitement,
- Le droit pour la personne d'**exprimer son point de vue**,
- Le droit de **contester la décision**.

Le mandat couvre ces droits via :

- `human_oversight.regime: "human_in_the_loop"` qui impose une intervention humaine pour toute proposition de décision,
- La note explicite `review_capacity` qui précise qu'une revue se résumant à un clic systématique ne constitue pas une intervention humaine significative,
- `contestation_channel` (présent dans les variantes restrictive et balanced) qui matérialise un canal de recours pour la personne.

**Position des autorités** : la CNIL et le Comité européen de la protection des données ont rappelé à plusieurs reprises que la conformité à l'article 22 ne peut pas se réduire à une validation formelle. La revue humaine doit être **significative**, donc disposer du temps, de la formation et de la capacité à infirmer la proposition.

## Article 30 — Registre des activités de traitement

Tout traitement doit être inscrit au registre. Le déploiement de l'agent dans la chaîne crédit ou comptable constitue un traitement nouveau ou modifié. Le mandat doit être référencé dans le registre, avec notamment :

- La finalité (assistance équipe finance, scoring, premiere ligne LCB-FT),
- La base légale identifiée,
- Les catégories de personnes concernées et de données traitées,
- Les durées de conservation,
- Les destinataires des données,
- Les mesures de sécurité.

Le mandate.yaml peut servir de référentiel pour le registre, sans s'y substituer.

## Article 32 — Sécurité du traitement

Le mandat impose des mesures techniques et organisationnelles via :

- `audit_trail.tamper_evidence: "sha256_chain"` (intégrité des journaux),
- `data_access.transfer_outside_eu: false` (pas de transfert hors UE par défaut),
- `expiration.revocation.immediate_triggers` qui incluent l'incident de sécurité confirmé.

## Article 33 et 34 — Notification de violation

En cas de violation susceptible d'engendrer un risque pour les droits et libertés des personnes, notification à la CNIL dans les 72 heures et information éventuelle des personnes concernées. Cette obligation s'articule avec la notification d'incident DORA aux autorités sectorielles (ACPR) lorsque l'entité est dans le périmètre.

## Article 35 — Analyse d'impact (DPIA)

Une DPIA est obligatoire pour les traitements à risque élevé. Le scoring de crédit envers une personne physique relève quasi systématiquement de cette obligation au titre de :

- L'article 35(3)(a) : évaluation systématique et approfondie d'aspects personnels qui sert de base à des décisions produisant des effets juridiques,
- La liste CNIL des traitements pour lesquels une DPIA est requise (publiée au JORF), qui inclut le scoring de crédit.

Le mandat documente le statut DPIA via `principal.dpia_required` qui doit être renseigné `oui` avec référence interne pour tout déploiement scoring.

**À VALIDER PAR JURISTE** : la DPIA doit être réalisée **avant** le déploiement, pas après. Une DPIA produite après le démarrage d'un traitement à risque élevé constitue un manquement, indépendamment de sa qualité intrinsèque.

## Articulation avec le pivot enforcement AMR

Le runtime AMR contribue à l'effectivité de l'article 22 : sans mandat valide qui autorise explicitement une proposition de décision, aucun token n'est émis et l'agent ne peut pas produire de proposition. La supervision humaine n'est plus une vérification a posteriori mais une condition d'émission du token. C'est cette mécanique structurelle qui distingue AMR d'un outil d'audit ou de certification.
