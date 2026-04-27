# Guide de déploiement — Agent Juridique & Veille

Ce guide résume les étapes de mise en production du template dans un service juridique, un cabinet d'avocats ou un service compliance. Il ne remplace pas une revue interne par le directeur juridique, le bâtonnier compétent (pour les avocats) ou le DPO.

## Préalables

- Un registre AMR installé (Tier 0 open-source ou Tier 1 mandate-gated avec `issue_action_token`).
- Un agent IA déjà déployé en interne ou fourni par un prestataire, avec un identifiant stable et des informations claires sur le modèle utilisé et son fournisseur.
- Un responsable habilité à signer le mandat (directeur juridique, associé responsable, bâtonnier d'arrondissement pour un cabinet d'avocats).
- Un DPO ou référent RGPD disponible pour relire le mandat avant signature.
- Une cartographie à jour des dossiers et clients pour identifier les périmètres exclus du champ d'action de l'agent.

## Étape 1 — Adapter le template maître

1. Ouvrir `mandate.yaml`.
2. Remplacer toutes les valeurs entre `< >` par les valeurs de l'organisation, en particulier l'identité du mandant, les sources autorisées propres au secteur, et les périmètres exclus.
3. Choisir le profil de base parmi les trois exemples fournis (`permissif`, `restrictif`, `équilibré`) et fusionner avec le template maître si besoin.
4. Vérifier la cohérence des volumes (`max_volume_per_day`) avec la charge prévue de veille.
5. Lister explicitement les périmètres clients ou dossiers **exclus** du champ de l'agent. C'est le point critique pour le secret professionnel.
6. Faire relire par le DPO et, si applicable, par le bâtonnier compétent.

## Étape 2 — Revue juridique interne

- Vérifier l'applicabilité de l'article 50 de l'AI Act sur la transparence vis-à-vis des utilisateurs internes qui dialoguent avec l'agent.
- Vérifier que l'usage prévu ne bascule pas vers l'Annexe III (cas de bascule possible : aide à la décision judiciaire, scoring de personnes, recommandation de licenciement).
- Documenter le test de mise en balance pour la base légale d'intérêt légitime (RGPD, article 6(1)(f)) si elle est retenue.
- Décider si une analyse d'impact (DPIA, article 35) est nécessaire, en particulier si la veille traite à grande échelle de jurisprudence nominative ou de données sensibles au sens de l'article 9 du RGPD.
- Pour un cabinet d'avocats, vérifier l'articulation avec les articles 21.6.3 et 21.6.4 du RIN sur les outils numériques et le cloisonnement des dossiers clients.

## Étape 3 — Information des parties prenantes

- **Utilisateurs internes** (juristes, avocats collaborateurs, juniors) : leur communiquer la notice prévue à l'article 50 de l'AI Act sur l'usage d'un agent IA dans le service. Préciser ce que l'agent peut produire et ce qu'il ne peut pas.
- **Clients du cabinet** (pour les avocats) : si l'agent peut être amené à traiter des informations issues de dossiers clients, mention dans la lettre de mission ou les conditions générales d'engagement de cabinet.
- **CSE** (pour les ETI) : consultation formelle si l'organisation en est dotée et si l'introduction de l'agent affecte les conditions de travail des juristes (Code du travail, articles L.2312-38 et L.2312-26).

## Étape 4 — Chargement du mandat dans AMR

1. Valider le YAML avec un parseur strict (`python -c "import yaml; yaml.safe_load(open('mandate.yaml'))"`).
2. Signer le mandat selon la politique de l'organisation (signature interne ou signature électronique eIDAS qualifiée).
3. Charger dans le registre AMR via le tool `create_mandate`.
4. Vérifier la présence de la chaîne avec `get_proof`.
5. Configurer l'agent pour qu'il appelle `verify_mandate` avant toute production de fiche, et `issue_action_token` avant toute action externe (publication, envoi, ouverture de ticket).

## Étape 5 — Tests de bout en bout

Avant la mise en production réelle :

- **Test de périmètre** : soumettre une demande hors périmètre (par exemple, un dossier client exclu ou une jurisdiction non autorisée), vérifier que l'agent refuse et escalade.
- **Test de cloisonnement** : faire interroger l'agent dans deux contextes clients différents, vérifier qu'il n'y a pas de fuite croisée.
- **Test de volume** : simuler un pic au-delà de `max_volume_per_day`, vérifier le blocage et l'alerte.
- **Test de qualification** : demander à l'agent un avis juridique direct, vérifier qu'il refuse et redirige vers un juriste humain.
- **Test de révocation** : révoquer le mandat, vérifier que l'agent cesse immédiatement d'agir et que `issue_action_token` refuse d'émettre.
- **Test d'audit** : exporter les journaux sur une période courte, vérifier l'intégrité SHA-256.

## Étape 6 — Checklist de validation avant mise en prod

- [ ] Mandat relu et signé par le responsable habilité.
- [ ] DPO consulté, DPIA réalisée si nécessaire.
- [ ] Pour un cabinet d'avocats : bâtonnier compétent informé si requis localement, articulation RIN validée.
- [ ] CSE informé et, le cas échéant, consulté.
- [ ] Notice transparence article 50 préparée et diffusée aux utilisateurs internes.
- [ ] Liste des dossiers et clients exclus du champ de l'agent à jour et chargée dans le mandat.
- [ ] Contrat de sous-traitance signé avec le fournisseur du modèle (RGPD, article 28).
- [ ] Procédure de gestion des demandes d'exercice de droits opérationnelle.
- [ ] Tests de bout en bout passés.
- [ ] Date de revue du mandat calée dans un calendrier (a minima annuelle).

## Points d'attention critiques

- **La qualification juridique reste un acte humain.** L'agent peut produire une fiche, proposer un score de criticité, suggérer une catégorisation. La qualification finale et la décision d'action engagent un juriste humain habilité. C'est un point disciplinaire pour les avocats et un point de responsabilité civile pour les juristes d'entreprise.
- **Le secret professionnel se protège par le cloisonnement, pas par les bonnes intentions.** Un agent qui accède à un dossier client doit être configuré pour qu'aucun élément de ce dossier ne contamine la mémoire de contexte ou les sorties produites pour un autre dossier. Le cloisonnement strict (`cross_tenant_isolation: strict` dans le mandat) est le minimum, à compléter par des contrôles techniques côté infrastructure.
- **Toute mise à jour majeure du modèle LLM** doit déclencher la révocation du mandat en cours et la signature d'un nouveau mandat. Un modèle n'est pas une variable libre, surtout dans un contexte juridique où la version exacte du modèle utilisé peut être demandée en cas de contestation.
- **Les transferts hors UE sont interdits par défaut dans le template.** Si le fournisseur du modèle les nécessite, encadrement par clauses contractuelles types et analyse de transfert spécifique (RGPD, articles 44 à 49).
- **La chaîne d'audit est inutile si personne ne la lit.** Prévoir une revue périodique par le directeur juridique ou un associé responsable, a minima trimestrielle pour les déploiements en cabinet d'avocats.

## Lien avec le runtime AMR

Ce template fournit la configuration que le tool `issue_action_token` du registre AMR utilise pour décider d'émettre ou non un jeton d'action signé Ed25519 lorsque l'agent veut agir. Pas de mandat actif couvrant l'action demandée, pas de jeton, pas d'action possible. La spécification complète est dans `docs/token-issuance-spec.md` du registre AMR sur GitHub.
