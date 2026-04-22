# Cartographie RGPD — Agent Marketing & Contenu

Référence : **Règlement (UE) 2016/679** du Parlement européen et du Conseil relatif à la protection des personnes physiques à l'égard du traitement des données à caractère personnel (RGPD).

## Base légale du traitement

Deux bases légales coexistent dans le périmètre marketing, et le mandat doit choisir explicitement l'une ou l'autre selon le canal et le pays de la personne :

- **Article 6, paragraphe 1, point f)** — intérêt légitime. Base par défaut pour la prospection de clients existants en B2B et pour la personnalisation de contenu sur les canaux propres (site web, espace client). Requiert un **test de mise en balance** documenté entre l'intérêt du responsable de traitement et les droits et libertés des personnes concernées (considérant 47 RGPD, lignes directrices CEPD 2024 sur l'intérêt légitime).
- **Article 6, paragraphe 1, point a)** — consentement. Base obligatoire pour la prospection électronique B2C en France (article L.34-5 du Code des postes et communications électroniques) et pour le suivi de comportement sur les sites web (cookies non strictement nécessaires, articles 82 de la loi Informatique et Libertés et lignes directrices CNIL).

Le gabarit retient l'intérêt légitime par défaut et documente une base alternative consentement. **Choix à valider par le DPO.**

## Information des personnes — Articles 12 à 14

L'article 13 du RGPD impose d'informer la personne au moment de la collecte. Pour un agent marketing, deux niveaux d'information se superposent :

1. **Notice RGPD complète** : politique de confidentialité du site, finalités marketing détaillées (segmentation, personnalisation, prospection), durée de conservation, droits, contact DPO. Responsabilité du déployeur, hors du mandat.
2. **Notice courte « agent IA »** : affichée en ouverture d'interaction conversationnelle au titre de l'article 50, paragraphe 1 du Règlement (UE) 2024/1689. Pour le contenu non-conversationnel (post social, article), le marquage de l'article 50, paragraphe 4 prend le relais.

Dans le template : section `agent.user_disclosure` pour le conversationnel, `agent.output_marking` pour le contenu publié.

## Profilage et droit d'opposition — Articles 4(4), 21 et 22

Si l'agent contribue à segmenter automatiquement une audience pour adresser des contenus différenciés, il participe à un **profilage** au sens de l'article 4, paragraphe 4 du RGPD. L'article 21, paragraphe 2 confère à la personne un droit d'opposition à tout moment au traitement à des fins de prospection, **y compris au profilage lié à cette prospection**. Ce droit ne peut pas être restreint par un intérêt légitime.

Dans le template : `data_access.categories` distingue les données agrégées anonymisées (segment_id, centre d'intérêt) des données nominatives (interdites en lecture pour l'agent). Le mandat doit s'articuler avec un mécanisme externe d'opt-out, généralement géré par l'outil de marketing automation.

L'article 22 du RGPD interdit, sauf exceptions, toute décision fondée exclusivement sur un traitement automatisé produisant des effets juridiques ou affectant significativement la personne. Un agent qui adresserait automatiquement une offre commerciale différenciée n'entre généralement pas dans le champ de l'article 22 (l'effet n'est pas significatif au sens du considérant 71). En revanche, un agent qui exclurait automatiquement une personne d'une offre, ou qui modulerait un prix de façon décisive, peut entrer dans ce champ. **À VALIDER PAR DPO.**

## Minimisation — Article 5, paragraphe 1, point c)

Le mandat liste explicitement les champs autorisés en lecture (`permissions.read.fields_allowed`) et les champs interdits (`fields_forbidden`). L'agent travaille par défaut sur des données d'audience **agrégées et anonymisées** (segment_id, centre d'intérêt, comportement agrégé). Les noms, adresses email, téléphones et identifiants individuels réconciliables sont exclus. La personnalisation nominative, si elle est activée, doit être traitée hors agent par l'outil d'envoi.

## Limitation de conservation — Article 5, paragraphe 1, point e)

Trois durées sont distinguées :

- **Brouillons et variantes générés** : 365 jours, pour traçabilité éditoriale et reconstitution du raisonnement de l'agent en cas de contestation d'un tiers.
- **Contenus publiés** : durée de vie commerciale du produit ou du service auquel ils se rapportent.
- **Données d'audience consultées** : alignement avec la politique générale du responsable de traitement (référentiel CNIL sur la prospection commerciale : trois ans à compter du dernier contact pour les prospects).

**À VALIDER PAR DPO** au regard du référentiel CNIL applicable au secteur.

## Sécurité du traitement — Article 32

Le template prévoit :

- Chaîne SHA-256 sur les journaux (`audit_trail.tamper_evidence: sha256_chain`) pour garantir l'intégrité.
- Accès aux journaux restreint à cinq rôles nominatifs.
- Interdiction de transfert hors UE (`restrictions.forbidden_actions`).
- Interdiction de réutilisation des contenus de marque pour entraîner un modèle tiers (`data_access.training_on_proprietary_data.allowed: false`).

## Analyse d'impact — Article 35

**DPIA non systématiquement obligatoire** pour le périmètre du gabarit (production de contenu). Elle devient obligatoire en cas de :

- Profilage à grande échelle utilisé pour évaluer ou prendre des décisions concernant les personnes (liste CNIL des traitements soumis à DPIA, point 1).
- Traitement à grande échelle de données sensibles (article 9).
- Croisement de jeux de données provenant de sources distinctes.

**À VALIDER PAR DPO** au regard du périmètre exact du déploiement.

## Articulation avec les directives ePrivacy et la loi Informatique et Libertés

- **Directive 2002/58/CE (ePrivacy)** transposée à l'**article 82 de la loi n° 78-17 du 6 janvier 1978 (Informatique et Libertés)** : le suivi sur terminal nécessite un consentement préalable. L'agent ne déclenche pas lui-même ces traceurs, mais ses sorties peuvent être servies sur des pages soumises à ce régime.
- **Article L.34-5 du Code des postes et communications électroniques** : prospection électronique vers une personne physique (B2C) interdite sans consentement préalable, sauf produits ou services analogues à ceux déjà fournis.

## Points à valider par un juriste ou un DPO

- Choisir entre intérêt légitime et consentement selon le canal et le pays.
- Documenter le test de mise en balance si l'intérêt légitime est retenu.
- Vérifier que l'agent ne bascule pas sous l'article 22 par effet de bord (segmentation décisive).
- Valider la durée de conservation des brouillons au regard du référentiel sectoriel.
- Vérifier la conformité du marquage des contenus avec l'article 50, paragraphe 4 de l'AI Act.
