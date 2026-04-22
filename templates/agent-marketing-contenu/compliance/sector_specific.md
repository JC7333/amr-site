# Règles sectorielles — Agent Marketing & Contenu

Ce document liste les règles additionnelles à vérifier selon le secteur d'activité du déployeur et la nature du contenu produit. Le gabarit de mandat est secteur-neutre ; il doit être complété par les obligations sectorielles applicables.

## Principe transversal — Propriété intellectuelle

- **Article L.122-4 du Code de la propriété intellectuelle** : « Toute représentation ou reproduction intégrale ou partielle faite sans le consentement de l'auteur […] est illicite. » L'agent ne peut reproduire ni transformer une œuvre protégée sans licence.
- **Article L.122-5 du Code de la propriété intellectuelle** : exceptions, dont la **citation brève** au paragraphe 3, point a) — sous condition de mention de la source et du nom de l'auteur, finalité critique, polémique, pédagogique, scientifique ou d'information, et caractère bref proportionné à la finalité.
- **Article L.335-2 du Code de la propriété intellectuelle** : la contrefaçon est punie de **3 ans d'emprisonnement et 300 000 € d'amende**, portée à 7 ans et 750 000 € en bande organisée.
- **Article L.713-2 du Code de la propriété intellectuelle** : interdiction de l'usage non autorisé d'une marque enregistrée pour des produits ou services identiques ou similaires.

Dans le mandat : `restrictions.forbidden_actions` exclut explicitement la reproduction d'œuvre protégée et la citation de marque tierce sans autorisation documentée.

## Principe transversal — Pratiques commerciales

- **Article L.121-1 du Code de la consommation** : interdiction des pratiques commerciales déloyales, dont les pratiques trompeuses (article L.121-2) et agressives (article L.121-6).
- **Article L.132-2 du Code de la consommation** : sanctions des pratiques trompeuses jusqu'à **300 000 €** pour une personne physique, **1,5 M€** pour une personne morale, montant pouvant être porté à **10 % du chiffre d'affaires moyen annuel calculé sur les trois derniers exercices**.
- **Article L.121-4 du Code de la consommation** : liste noire des pratiques réputées trompeuses en toutes circonstances. Inclut notamment toute affirmation inexacte sur les caractéristiques essentielles d'un produit ou d'un service.

Dans le mandat : `restrictions.forbidden_actions` exclut les claims chiffrés non sourcés et les promesses de résultat non garanti.

## Principe transversal — Concurrence

- **Article L.122-1 du Code de la consommation** : la publicité comparative est licite sous conditions strictes (objectivité, vérifiabilité, non-dénigrement). Le gabarit interdit par défaut la comparaison nominative avec un concurrent (`scope.excluded_processes`).

## Plateformes en ligne et publicité ciblée

- **Règlement (UE) 2022/2065 (Digital Services Act)** :
  - **Article 26** : transparence de la publicité en ligne — l'utilisateur doit pouvoir identifier qu'il s'agit d'une publicité, qui en est à l'origine, et sur quels paramètres principaux il a été ciblé.
  - **Article 28** : protection renforcée des mineurs, interdiction du ciblage publicitaire fondé sur le profilage des mineurs.
  - **Article 39** : registre public des publicités pour les très grandes plateformes en ligne.
- Si l'organisation est une plateforme intermédiaire, ces obligations s'ajoutent au mandat. Sinon, elles concernent l'écosystème dans lequel les contenus sont diffusés et doivent être anticipées.

## E-commerce et vente à distance

- **Article L.111-1 du Code de la consommation** : obligation précontractuelle d'information sur les caractéristiques essentielles, le prix et la durée du contrat. Une fiche produit générée par l'agent doit respecter cette obligation au pixel près.
- **Article L.221-5 du Code de la consommation** : information préalable obligatoire dans le cadre des contrats à distance. **À VALIDER PAR JURISTE** si l'agent rédige des fiches produits transactionnelles.

## Services financiers et assurance

- **Code monétaire et financier, article L.533-12** : obligation de communication claire, exacte et non trompeuse. La publicité sur un service d'investissement est soumise au visa ou à la déclaration ACPR/AMF selon les cas.
- **Code monétaire et financier, article L.341-3** : règles strictes de démarchage bancaire et financier.
- **Code des assurances, article L.521-1** : devoir d'information et de conseil de l'intermédiaire d'assurance.
- **Recommandation ACPR 2023-R-01** relative à la gouvernance des algorithmes : à intégrer dans le mandat sous forme de points de contrôle humains.
- **Profil restrictif** (`examples/02-restrictif.yaml`) recommandé pour ce secteur en première intention.

## Santé, dispositifs médicaux et médicaments

- **Code de la santé publique, article L.5122-1 et suivants** : la publicité pour les médicaments est strictement encadrée, contrôle préalable de l'ANSM pour le grand public.
- **Code de la santé publique, article L.5213-1 et suivants** : règles spécifiques pour la publicité des dispositifs médicaux.
- **Décret n° 2017-1417 du 28 septembre 2017** : encadrement de la communication des établissements de santé.
- **Article L.4113-9 du Code de la santé publique** : interdiction de toute publicité directe ou indirecte par les professionnels de santé hors mentions autorisées.
- L'agent doit exclure tout contenu de promotion santé directe et passer par le template santé dédié pour ce secteur.

## Tabac, alcool, jeux d'argent

- **Loi n° 91-32 du 10 janvier 1991 (loi Évin)** : interdiction de toute publicité indirecte pour le tabac ; règles strictes pour l'alcool (mentions obligatoires, supports limitatifs).
- **Code de la santé publique, article L.3323-2** : limitation des supports autorisés pour la publicité d'alcool.
- **Code de la sécurité intérieure, article L.320-12** : encadrement strict de la publicité des opérateurs de jeux.
- L'agent doit exclure ces secteurs sauf paramétrage explicite et validation juridique.

## Immobilier

- **Loi n° 70-9 du 2 janvier 1970 (loi Hoguet)** et son décret d'application : règles d'affichage des annonces immobilières (prix, honoraires, surface loi Carrez).
- **Arrêté du 10 janvier 2017** sur l'information précontractuelle relative aux honoraires.
- **À VALIDER PAR JURISTE** si l'agent rédige des annonces immobilières — risque de DGCCRF élevé.

## Secteur public et marchés publics

- **Code des relations entre le public et l'administration, article L.311-3-1** : obligation d'information sur l'usage d'un traitement algorithmique fondant une décision individuelle. À combiner avec l'article 50 de l'AI Act.
- Communication institutionnelle d'État ou de collectivité : règles d'affichage de la marque État ou des collectivités (charte communication gouvernementale).

## Mineurs et publics vulnérables

- **Code de la consommation, article L.121-21** : protection renforcée des consommateurs vulnérables.
- **Article 28 du DSA** : interdiction du ciblage publicitaire des mineurs sur les plateformes intermédiaires.
- **Recommandations ARPP** : encadrement déontologique de la communication à destination des enfants.

Le mandat exclut par défaut la production de contenu à destination des mineurs sans supervision (`restrictions.forbidden_actions`).

## Points à valider par un juriste

- Confirmer le rattachement sectoriel et lister les régulateurs sectoriels concernés (DGCCRF, ARPP, ACPR, AMF, ANSM, Arcom, CNIL).
- Établir et tenir à jour la **liste blanche des marques tierces** dont la mention est autorisée (presse, partenariats, citations clients avec accord écrit).
- Vérifier les chartes éditoriales et de marque internes ; les annexer au mandat.
- Auditer l'outil de marketing automation et le CMS pour la traçabilité des publications validées par l'humain.
