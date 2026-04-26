# Cartographie AI Act — Template Finance & Comptable

Ce document cartographie le mandat avec le **Règlement (UE) 2024/1689** dit « AI Act ». Il a vocation à être joint au registre interne des systèmes d'IA et présenté en cas de contrôle.

## Classification du système

Un agent qui réalise du scoring de crédit ou évalue la solvabilité d'une personne physique relève explicitement de l'**Annexe III, point 5(b)** : *« systèmes d'IA destinés à être utilisés pour évaluer la solvabilité de personnes physiques ou pour établir leur score de crédit »*. Il est classé **système à haut risque**.

Un agent qui se limite au lettrage comptable, au contrôle de cohérence sur écritures internes ou à la première ligne LCB-FT (sans décision sur personne physique) ne relève pas stricto sensu de l'Annexe III. Il reste néanmoins soumis aux obligations générales de transparence (Article 13) et de tenue de registres (Article 12) en bonne pratique.

**À VALIDER PAR JURISTE** : la classification fine dépend du périmètre exact d'action de l'agent dans l'organisation. Un agent multi-domaine (cf. exemple `balanced.yaml`) sera classé haut risque dès lors qu'au moins un de ses scopes touche au scoring de personne physique.

## Articles applicables

### Article 12 — Tenue de registres automatiques

L'agent doit générer automatiquement des journaux d'événements pendant son fonctionnement. La rétention doit permettre de retracer chaque action proposée et chaque décision humaine prise sur cette proposition.

Le mandat couvre cet article via la section `audit_trail` qui définit `logged_events`, `log_retention_days` et `tamper_evidence: sha256_chain`. La chaîne de hash garantit l'intégrité des journaux et leur opposabilité.

### Article 13 — Transparence vis-à-vis des déployeurs

Les utilisateurs en aval doivent disposer d'une notice claire sur les capacités, limites et conditions d'usage du système. Le mandat fournit cette notice via le `README.md` et la section `agent.purpose` du mandate.yaml.

### Article 14 — Supervision humaine effective

C'est l'article central pour ce template. La supervision humaine doit être **effective**, ce qui suppose :

- Une personne formée et habilitée à intervenir sur la décision,
- Un canal de contestation accessible à la personne concernée,
- Une capacité réelle de l'opérateur humain à infirmer la proposition de l'agent (pas un simple clic systématique).

Le mandat couvre l'article 14 via `human_oversight.regime: "human_in_the_loop"`, `mandatory_review_triggers` chiffrés, `reviewer_profile.training_required: true`, et la note explicite `review_capacity` qui rappelle qu'une revue qui se réduit à un clic systématique ne constitue pas une intervention humaine significative au sens de l'article 22 RGPD ni de l'article 14 AI Act.

### Article 26 — Obligations du déployeur

Le déployeur (l'organisation qui utilise le système) doit s'assurer que :

- Le système est utilisé conformément à sa notice,
- Les données d'entrée sont pertinentes et représentatives,
- La supervision humaine est assurée par un personnel compétent,
- Les journaux sont conservés pendant la durée requise,
- Les autorités sont informées en cas d'incident grave.

Le mandat documente ces obligations dans la section `principal` (responsabilité du mandant), `human_oversight.reviewer_profile` (compétence du personnel), `audit_trail` (journaux) et `expiration.revocation.immediate_triggers` (déclencheurs de révocation incluant l'incident de sécurité).

### Article 27 — Analyse d'impact sur les droits fondamentaux (FRIA)

Pour les systèmes à haut risque utilisés par certaines entités (notamment les organismes publics et certaines entités privées sur des services essentiels), une analyse d'impact sur les droits fondamentaux est requise avant déploiement.

**À VALIDER PAR JURISTE** : l'application de l'article 27 aux fintechs et établissements de crédit privés relève d'une lecture combinée avec le considérant 96. Les opérateurs de scoring de crédit B2C devraient considérer la réalisation d'une FRIA en bonne pratique.

### Article 99 — Sanctions administratives

Les sanctions sont calibrées selon la gravité du manquement :

- Jusqu'à **35 M€ ou 7 % du chiffre d'affaires mondial** pour mise sur le marché ou utilisation de systèmes d'IA interdits (Article 5).
- Jusqu'à **15 M€ ou 3 % du chiffre d'affaires mondial** pour manquement aux obligations sur systèmes à haut risque (Articles 9 à 27), ce qui couvre le scoring de crédit.
- Jusqu'à **7,5 M€ ou 1 % du chiffre d'affaires mondial** pour fourniture d'informations inexactes aux autorités.

## Calendrier d'application

L'AI Act est entré en vigueur le **1er août 2024**. Les obligations sur systèmes à haut risque relevant de l'Annexe III (dont le scoring de crédit) entrent en application le **2 août 2026**.

**Report potentiel via Digital Omnibus** : les trilogues européens en cours (au 25 avril 2026) projettent un report de l'entrée en application de l'Annexe III au **2 décembre 2027**. Ce report n'est **pas arrêté en droit positif** au moment de la rédaction de ce template. Le mandat AMR adopte la posture *« préparer les deux scénarios »* : la conformité doit être atteignable pour le 2 août 2026 et restera applicable si le report est confirmé.

**À SUIVRE** : statut final du Digital Omnibus.

## Articulation avec le pivot enforcement AMR

Le runtime AMR fournit la couche d'exécution du mandat. Le tool MCP `issue_action_token` n'émet un jeton d'action signé en Ed25519 que si :

1. Un mandat actif couvre la classe d'action demandée,
2. Le scope du mandat inclut l'action précise,
3. Les plafonds journaliers ne sont pas dépassés,
4. Les triggers de supervision humaine sont respectés (validation préalable obtenue si requise).

Sans token, l'agent ne peut pas exécuter l'action. C'est un verrou structurel avant l'acte, pas un audit après. Cette mécanique correspond à l'esprit de l'article 14 AI Act : la supervision humaine n'est pas une vérification a posteriori, c'est une condition d'autorisation préalable.
