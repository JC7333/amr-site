# Cartographie RGPD — Agent Support Client

Référence : **Règlement (UE) 2016/679** du Parlement européen et du Conseil relatif à la protection des personnes physiques à l'égard du traitement des données à caractère personnel (RGPD).

## Base légale du traitement

La base légale retenue dans le template est l'**article 6, paragraphe 1, point b)** — traitement nécessaire à l'exécution du contrat auquel la personne concernée est partie. C'est le fondement naturel pour un agent qui traite une demande client portant sur un produit ou un service souscrit.

Une base alternative sur l'**article 6, paragraphe 1, point f)** (intérêt légitime) est documentée dans le gabarit pour les cas périphériques (amélioration du service, contrôle qualité). Cette base secondaire impose un **test de mise en balance** documenté entre l'intérêt du responsable de traitement et les droits et libertés de la personne concernée.

## Information des personnes — Articles 12 à 14

L'article 13 du RGPD impose d'informer la personne au moment de la collecte. Le template distingue deux niveaux d'information :

1. **Notice RGPD complète** : hébergée dans la politique de confidentialité du site, accessible à tout moment. Responsabilité du déployeur. Elle inclut les finalités, la base légale, la durée de conservation, les droits, le DPO.
2. **Notice courte « agent IA »** : affichée en ouverture de conversation, au titre de l'article 50 du Règlement (UE) 2024/1689. Elle signale l'interaction avec un système d'IA et l'option d'escalade humaine.

Dans le template : section `agent.user_disclosure` pour la notice courte. La notice RGPD longue n'est pas dans le mandat — elle relève de la politique générale du déployeur.

## Minimisation — Article 5, paragraphe 1, point c)

Le mandat liste explicitement les champs autorisés en lecture (`permissions.read.fields_allowed`) et les champs interdits (`fields_forbidden`). Les données bancaires en clair, les mots de passe, les données de santé, les opinions politiques et religieuses sont exclues par principe. Les champs non nécessaires au traitement de la demande sont absents du mandat.

## Limitation de conservation — Article 5, paragraphe 1, point e)

Trois durées sont distinguées :

- **Ticket actif** : 90 jours après fermeture, pour permettre la reprise d'un échange.
- **Ticket clos archivé** : 1095 jours (3 ans), alignement avec la prescription commerciale de l'**article 2224 du Code civil**.
- **Journaux techniques d'audit** : 1095 jours, même justification.

**À VALIDER PAR JURISTE** : certains secteurs (assurance, banque, télécoms avec clients vulnérables) imposent des durées plus longues au titre de règles sectorielles. Le gabarit fixe 3 ans comme plancher raisonnable.

## Sécurité du traitement — Article 32

Le template prévoit :

- Chaîne SHA-256 sur les journaux (`audit_trail.tamper_evidence: sha256_chain`) pour garantir l'intégrité.
- Accès aux journaux restreint à quatre rôles nominatifs.
- Interdiction de transfert hors UE (`restrictions.forbidden_actions`).
- Interdiction d'entraîner un modèle tiers sur les conversations clients.

## Décision automatisée — Article 22

L'agent de support client tel que cadré par ce template **ne produit pas** de décision automatisée produisant des effets juridiques ou affectant significativement la personne, dès lors que :

- Tout geste commercial au-delà du plafond passe par un humain.
- Toute résiliation est exclue du périmètre.
- Toute modification de données bancaires est exclue du périmètre.

Si le périmètre évolue (par exemple : l'agent décide unilatéralement d'un refus de remboursement), l'article 22 devient applicable et déclenche l'obligation de garantir à la personne le droit d'obtenir une intervention humaine et de contester la décision.

## Analyse d'impact — Article 35

**DPIA non obligatoire a priori** pour le périmètre du gabarit. Elle devient obligatoire en cas de :

- Traitement à grande échelle de données sensibles (article 9).
- Évaluation systématique produisant des effets juridiques.
- Combinaison avec d'autres critères de la liste CNIL des traitements soumis à DPIA.

**À VALIDER PAR DPO** au regard du périmètre exact du déploiement.

## Points à valider par un juriste

- Vérifier l'articulation du test de mise en balance si la base légale secondaire (intérêt légitime) est retenue.
- Valider la durée de conservation au regard des règles sectorielles applicables.
- Vérifier la rédaction de la notice RGPD longue et la cohérence avec la notice courte article 50.
- Confirmer que l'agent ne bascule pas sous l'article 22 par effet de bord.
