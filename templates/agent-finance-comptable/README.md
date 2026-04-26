# Template AMR — Agent Finance & Comptable

Template de mandat prêt à l'emploi pour encadrer un agent IA déployé dans un contexte financier ou comptable (scoring de crédit, BNPL, lettrage automatique, contrôle de cohérence comptable, génération de reportings réglementaires, première analyse LCB-FT).

## Pour qui

- Directeurs financiers et responsables comptables qui testent un agent en assistance équipe finance.
- Fintechs, plateformes BNPL, prestataires de paiement et établissements de crédit qui déploient un agent en cycle d'octroi.
- Compliance officers et responsables LCB-FT qui doivent encadrer un agent en première ligne d'analyse.
- Cabinets d'expertise comptable qui livrent un service d'analyse augmenté à leurs clients.

## Contexte

Les processus financiers et comptables touchent à trois zones de risque cumulées : la décision individuelle automatisée envers une personne (crédit, scoring), la stabilité opérationnelle d'un service essentiel (paiement, comptes) et la sincérité comptable opposable au régulateur fiscal et prudentiel.

Plusieurs cadres se superposent :

- Le **Règlement (UE) 2024/1689** dit « AI Act » classe en haut risque les systèmes utilisés pour évaluer la solvabilité d'une personne physique ou établir son score de crédit (Annexe III, point 5(b)). La supervision humaine effective (article 14), les obligations du déployeur (article 26) et la tenue de registres (article 12) s'appliquent pleinement.
- Le **Règlement (UE) 2022/2554** dit « DORA » impose aux entités financières un cadre de gestion du risque informatique, de gestion des prestataires tiers critiques et de notification d'incident. Il est applicable depuis le 17 janvier 2025.
- Le **Règlement (UE) 2016/679** dit « RGPD » encadre les décisions individuelles automatisées (article 22) et impose une intervention humaine significative pour les décisions produisant des effets juridiques sur la personne, ce qui couvre l'octroi de crédit.
- Le **Code monétaire et financier**, articles L.561-1 et suivants, transpose les obligations de lutte contre le blanchiment et le financement du terrorisme (LCB-FT) sous la supervision de l'ACPR et de Tracfin.
- Les normes **IFRS** ou le **Plan comptable général** s'imposent selon la taille et le statut de l'entité pour la comptabilité officielle. Toute écriture comptable produite par un agent doit rester traçable à un opérateur humain habilité.

Déployer un agent sur la chaîne crédit, paiement ou comptable sans mandat documenté, c'est exposer l'organisation à une décision automatisée non rattachée à un mandant humain, à un défaut de piste d'audit opposable au régulateur, et à un risque réputationnel direct si une personne physique conteste une décision.

## Trois exemples de déploiement concret

1. **Première analyse de dossier crédit BNPL** : l'agent reçoit la demande, vérifie la cohérence des documents fournis, qualifie le risque selon une grille préétablie, propose une décision. La décision finale d'octroi ou de refus est validée par un opérateur humain habilité, conformément à l'article 22 du RGPD. Aucun engagement n'est pris par l'agent seul.
2. **Lettrage automatique et contrôle de cohérence** : l'agent rapproche les écritures bancaires des factures fournisseurs et clients, signale les écarts, propose des écritures de régularisation. Toute écriture comptable est validée par un comptable humain avant inscription au grand livre.
3. **Première ligne LCB-FT et alerte sur transactions atypiques** : l'agent applique les règles de surveillance des transactions, élève une alerte vers le responsable LCB-FT lorsque les seuils sont dépassés ou qu'une typologie suspecte est détectée. La décision de déclaration de soupçon à Tracfin reste exclusivement humaine.

## Ce que ce template fournit

- `mandate.yaml` : le mandat structuré prêt à charger dans un registre AMR, avec périmètre d'action, plafonds chiffrés, restrictions explicites sur la décision individuelle automatisée, seuils de supervision humaine, durée de validité, cartographie AI Act, RGPD et règles sectorielles finance.
- `examples/` : trois variantes (permissive, restrictive, équilibrée) commentées, pour s'adapter au type d'activité (assistance comptable interne, scoring crédit BNPL, première ligne LCB-FT).
- `compliance/` : trois fiches courtes qui cartographient le mandat avec l'AI Act, le RGPD et les règles sectorielles finance (DORA, LCB-FT, ACPR, IFRS).
- `deploy_guide.md` : checklist de mise en production et points d'attention critiques.

## Lien avec le pivot enforcement AMR

Ce template fournit la configuration de mandat que le tool MCP `issue_action_token` utilisera pour émettre les jetons d'action signés en Ed25519 lors du runtime. Le mandat décrit ce qui est autorisé ; le runtime AMR n'émet un token que si le mandat est actif et couvre l'action demandée dans son scope. Pas de mandat valide, pas de token, pas d'action possible.

C'est un verrou structurel avant l'acte, pas un audit après. La spécification d'émission est documentée dans `docs/token-issuance-spec.md` du registre AMR.

## Pourquoi c'est risqué sans mandat

Un agent qui décide ou pré-décide dans la chaîne financière sans mandat documenté expose l'organisation à plusieurs risques concrets :

- **Sanctions AI Act** : jusqu'à 35 M€ ou 7 % du chiffre d'affaires mondial pour les manquements les plus graves (article 99). Jusqu'à 15 M€ ou 3 % pour les manquements aux obligations sur systèmes à haut risque, dont relèvent le scoring de crédit et l'évaluation de solvabilité (Annexe III, point 5).
- **Sanctions RGPD** : jusqu'à 20 M€ ou 4 % du chiffre d'affaires mondial pour défaut d'intervention humaine significative sur une décision automatisée produisant des effets juridiques (article 83.5).
- **Sanctions DORA et ACPR** : sanctions administratives et financières par les autorités sectorielles en cas de défaut de gestion du risque IT ou de notification d'incident (Règlement UE 2022/2554, articles 50 et 54).
- **Sanctions LCB-FT** : sanctions disciplinaires et financières de l'ACPR en cas de défaillance du dispositif de surveillance et de déclaration (Code monétaire et financier, articles L.561-36 et suivants).
- **Risque civil et contractuel** : un client lésé par une décision de crédit automatisée non encadrée dispose d'un recours direct, indépendamment des sanctions réglementaires.

Le mandat AMR ne supprime pas ces risques — il les **encadre**, les **documente** et les **rend opposables**.

## Positionnement tarifaire indicatif

Template vendu en pack clé en main, entre **3 500 € et 5 000 €** selon le niveau d'adaptation. Tarification haute justifiée par l'empilement réglementaire (AI Act haut risque + DORA + RGPD article 22 + LCB-FT) :

- **Pack standard (3 500 €)** : les fichiers tels quels, licence d'usage interne, une heure d'accompagnement à la configuration.
- **Pack adapté (4 500 €)** : personnalisation du mandat aux outils internes (cœur bancaire, ERP comptable, outil de scoring) et aux procédures de contrôle interne de l'organisation.
- **Pack intégré (5 000 €)** : déploiement dans un runtime AMR Tier 1, connexion aux systèmes de scoring et de surveillance, première revue de conformité avec le compliance officer ou le responsable LCB-FT.

Le template seul ne remplace pas le runtime mandate-gated (Tier 1 AMR, 350 €/mois) ni une revue par un compliance officer. Il pose la structure ; la décision d'autoriser un agent à intervenir dans la chaîne crédit ou comptable reste humaine.

## À valider côté client avant déploiement

- Revue du mandat par le compliance officer et le responsable LCB-FT.
- Test de mise en balance documenté pour la base légale d'intérêt légitime (article 6(1)(f) RGPD), en particulier pour le scoring.
- DPIA (article 35 RGPD) pour les traitements à risque élevé, ce qui couvre quasi systématiquement le scoring de crédit.
- Notification préalable au registre des prestataires tiers critiques DORA si l'agent ou son fournisseur entre dans le périmètre.
- Validation par le contrôle interne et alignement avec la cartographie des risques opérationnels.
- Mise à jour du registre des traitements RGPD et de la documentation LCB-FT.
