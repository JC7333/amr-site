# Template AMR — Agent Juridique & Veille

Template de mandat prêt à l'emploi pour encadrer un agent IA déployé en assistance à la veille juridique, réglementaire et jurisprudentielle (monitoring de Légifrance, EUR-Lex, jurisprudence Cassation, alertes des autorités sectorielles, priorisation d'alertes compliance, rédaction de fiches de synthèse).

## Pour qui

- Directions juridiques d'ETI et de grands comptes qui industrialisent leur veille en complément du travail des juristes.
- Cabinets d'avocats qui automatisent une partie de la veille de service ou la veille client externalisée.
- Responsables compliance qui surveillent les évolutions réglementaires sectorielles (banque-finance, assurance, santé, télécoms, énergie, défense).
- DPO et compliance officers qui doivent intégrer rapidement les nouvelles obligations sectorielles dans leurs registres.

## Contexte

La veille juridique est, par nature, un travail de capture exhaustive d'informations publiques suivi d'une qualification fine par un juriste. Un agent IA peut absorber la première moitié sans difficulté technique. La qualification, elle, reste un acte juridique qui engage la responsabilité civile et professionnelle d'un humain habilité.

Plusieurs cadres se superposent dès qu'un agent intervient dans cette chaîne :

- Le **Règlement (UE) 2024/1689** dit « AI Act » impose des obligations de transparence (article 50) lorsque l'agent interagit directement avec des personnes physiques (chatbot interne d'un service juridique, par exemple). La veille pure reste rarement classée à haut risque au sens de l'Annexe III, sauf si elle alimente une décision affectant des personnes (recommandation de licenciement, refus de contrat, scoring de risque sur un tiers identifiable).
- Le **Règlement (UE) 2016/679 (RGPD)** s'applique dès lors que l'agent traite des données personnelles, ce qui couvre quasi systématiquement la jurisprudence (les décisions de justice nomment des parties).
- Le **Règlement Intérieur National** (RIN) de la profession d'avocat encadre l'usage d'outils tiers en cabinet, le secret professionnel, et la confidentialité client. L'article 21.6.3 du RIN sur les outils numériques s'applique dès qu'un agent traite des données client.
- Le **Code de déontologie des avocats** (décret n° 2005-790 modifié) impose la confidentialité et la diligence professionnelle.
- Le **secret professionnel** de l'article 226-13 du Code pénal protège les informations confiées au juriste.

Déployer un agent de veille sans mandat documenté, c'est laisser la machine consommer des données sensibles, produire des qualifications qui peuvent être prises pour des avis juridiques, et publier des synthèses sans borne sur le périmètre exclu.

## Trois exemples de déploiement concret

1. **Veille législative et réglementaire automatisée** : l'agent monitore Légifrance, le Journal officiel, EUR-Lex, les sites de l'AMF, l'ACPR, la CNIL, l'ANSSI, l'ARCOM. Il identifie les textes nouveaux pertinents pour l'organisation à partir d'une grille de mots-clés et de domaines, produit une fiche de synthèse, propose un niveau de criticité. La validation et la qualification juridique fine sont assurées par un juriste humain.

2. **Suivi de jurisprudence sectorielle** : l'agent surveille les bases publiques de jurisprudence (Cassation, Conseil d'État, ECLI européen, cours d'appel via Légifrance), repère les arrêts impactants pour un secteur cible défini, alerte avec un score d'impact estimé. La lecture juridique de l'arrêt et la décision d'en tirer une note interne ou un avis client restent humaines.

3. **Priorisation d'alertes compliance** : l'agent reçoit les alertes brutes des autorités sectorielles (sanctions, lignes directrices, recommandations), les classe par criticité et par périmètre fonctionnel impacté, propose la création d'un ticket de suivi. La décision d'engager une revue interne, de notifier le management ou de déclencher une analyse d'impact reste humaine.

## Ce que ce template fournit

- `mandate.yaml` : le mandat structuré prêt à charger dans un registre AMR, avec périmètre de veille, sources autorisées, restrictions explicites sur la qualification juridique automatique, seuils d'escalade, durée de validité, cartographie AI Act, RGPD et règles déontologiques.
- `examples/` : trois variantes (permissive, restrictive, équilibrée) commentées, pour s'adapter au type de structure (direction juridique interne, cabinet d'avocats, service compliance d'un opérateur réglementé).
- `compliance/` : trois fiches courtes qui cartographient le mandat avec l'AI Act, le RGPD et les règles sectorielles propres au monde juridique (RIN, secret professionnel, diligence).
- `deploy_guide.md` : checklist de mise en production et points d'attention sur l'articulation avec la responsabilité professionnelle des juristes.

## Lien avec le pivot enforcement AMR

Ce template fournit la configuration de mandat que le tool MCP `issue_action_token` utilisera pour émettre les jetons d'action signés en Ed25519 lors du runtime. Le mandat décrit ce qui est autorisé ; le runtime AMR n'émet un token que si le mandat est actif et couvre l'action demandée dans son scope. Pas de mandat valide, pas de token, pas d'action possible.

C'est un verrou structurel avant l'acte, pas un audit après. Pour la veille juridique, cela signifie qu'aucune diffusion automatique de fiche externe, aucune réponse engageante à un client interne, aucune publication sur un canal partagé ne peut se déclencher si le mandat ne couvre pas explicitement cette catégorie d'action. La spécification d'émission est documentée dans `docs/token-issuance-spec.md` du registre AMR.

## Pourquoi c'est risqué sans mandat

Un agent de veille juridique sans mandat documenté expose l'organisation à plusieurs risques concrets :

- **Qualification juridique non encadrée** : une note de synthèse produite par l'agent peut être lue comme un avis juridique par un destinataire interne. Si elle est fausse et qu'elle a guidé une décision dommageable, la responsabilité du juriste superviseur est engagée même si l'agent a écrit la note.
- **Atteinte au secret professionnel** : un agent qui consomme un dossier client sans cloisonnement strict peut faire fuiter des éléments confidentiels dans les contextes d'autres dossiers (fuite cross-tenant typique des LLM mal encadrés). Sanctions : article 226-13 du Code pénal, jusqu'à un an d'emprisonnement et 15 000 € d'amende, plus radiation possible.
- **Sanctions RGPD** : jusqu'à **20 M€ ou 4 %** du chiffre d'affaires mondial pour défaut d'information (articles 13, 14) ou conservation excessive de données issues de jurisprudence (article 5(1)(e)).
- **Sanctions AI Act article 50** : jusqu'à **15 M€ ou 3 %** du chiffre d'affaires mondial pour défaut d'information sur l'interaction avec une IA, lorsque l'agent dialogue avec des utilisateurs internes ou des clients.
- **Manquement déontologique pour les avocats** : sanctions disciplinaires pouvant aller jusqu'à la radiation pour usage non encadré d'outils tiers compromettant le secret professionnel.

Le mandat AMR ne supprime pas ces risques — il les **borne** (sources autorisées, types de production, périmètres clients exclus) et les **documente** (journal opposable, chaîne de mandats vérifiable).

## Positionnement tarifaire indicatif

Template vendu en pack clé en main, entre **2 500 € et 4 000 €** selon le niveau d'adaptation :

- **Pack standard (2 500 €)** : les fichiers tels quels, licence d'usage interne, une heure d'accompagnement à la configuration.
- **Pack adapté (3 200 €)** : personnalisation aux conventions internes du service juridique ou du cabinet, à la liste des sources surveillées, aux périmètres clients exclus.
- **Pack intégré (4 000 €)** : déploiement dans un runtime AMR Tier 1, connexion aux outils internes (DMS, CRM avocat, outils de veille existants), première revue de conformité avec un juriste partenaire.

Le template seul ne remplace pas le runtime mandate-gated (Tier 1 AMR, 350 €/mois) ni une validation par le service juridique ou le bâtonnier compétent pour les avocats. Il pose la structure ; la qualification juridique reste humaine et la responsabilité professionnelle aussi.

## À valider côté client avant déploiement

- Revue du mandat par le directeur juridique ou l'associé responsable du cabinet.
- Validation de la liste des sources autorisées et exclues, et de la liste des dossiers ou clients exclus du périmètre.
- Mise à jour de la notice d'information utilisée pour informer les utilisateurs internes du recours à un agent IA dans le service.
- Articulation avec les obligations de secret professionnel (article 226-13 du Code pénal, articles 21.6.3 et 21.6.4 du RIN pour les avocats).
- Décision sur la nécessité d'une analyse d'impact (DPIA) au titre de l'article 35 RGPD si la veille touche à des données sensibles ou à des personnes identifiables à grande échelle.
- Formation des juristes humains aux limites de l'agent et aux cas obligatoires d'escalade.
