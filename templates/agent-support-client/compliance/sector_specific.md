# Règles sectorielles — Agent Support Client

Ce document liste les règles additionnelles à vérifier selon le secteur d'activité du déployeur. Le gabarit de mandat est secteur-neutre ; il doit être complété par les obligations sectorielles applicables.

## Principe transversal — Droit commun

Deux règles s'appliquent quel que soit le secteur :

- **Article 1103 du Code civil** : « Les contrats légalement formés tiennent lieu de loi à ceux qui les ont faits. » Toute promesse tenue par l'agent (remboursement, délai, geste commercial) engage l'entreprise comme si elle avait été faite par un conseiller humain. Le mandat borne cet engagement par des plafonds chiffrés (`permissions.invoke.max_amount_eur`).
- **Article L.121-1 du Code de la consommation** : interdiction des pratiques commerciales déloyales. Un agent qui dissimulerait sa nature d'IA, ou qui tiendrait des propos trompeurs sur les caractéristiques d'un service, exposerait l'entreprise à une sanction pénale (article L.132-2 du même code).

## E-commerce et vente à distance

- **Article L.221-18 du Code de la consommation** : droit de rétractation de 14 jours pour les contrats conclus à distance. L'agent doit informer clairement le client qui en fait la demande.
- **Article L.111-1 du Code de la consommation** : obligation précontractuelle d'information sur les caractéristiques essentielles du bien ou service, le prix, la durée du contrat.
- **À VALIDER PAR JURISTE** si l'agent négocie des délais ou des réductions : bien cadrer l'offre et éviter l'ambiguïté sur le prix final.

## Services financiers et assurance

- **Code monétaire et financier, article L.533-11** : obligation de conseil adapté pour les prestataires de services d'investissement. Un agent ne peut formuler un conseil personnalisé sans supervision humaine.
- **Code des assurances, article L.521-1** : devoir d'information et de conseil de l'intermédiaire d'assurance. Interdiction de déléguer ce devoir à un agent non supervisé.
- **Règlement (UE) 2022/2554 (DORA)** applicable depuis janvier 2025 : exigences de résilience opérationnelle numérique, notamment sur la gestion des tiers TIC. Si le modèle LLM est hébergé par un tiers, il peut entrer dans le périmètre DORA.
- **Recommandation ACPR 2023-R-01 relative à la gouvernance des algorithmes** : à intégrer dans le mandat sous forme de points de contrôle humains.
- **Exemple 02 « restrictif »** : profil recommandé pour un premier déploiement dans ce secteur.

## Télécoms

- **Code des postes et communications électroniques, articles L.44 et suivants** : portabilité du numéro, changement d'opérateur — tout acte contractuel de résiliation ou portage doit être exclu du périmètre de l'agent, ce que fait le gabarit (`scope.excluded_processes`).
- **Arcep, décision n° 2020-1472** : règles relatives à la qualité de service — si l'agent formule un engagement sur un délai de raccordement, le respecter devient opposable.

## Santé (hors cas HDS direct, traité par le template santé)

- Si l'agent de support renvoie vers un professionnel de santé ou un parcours de soins, il ne doit pas formuler de conseil médical. Une clause explicite dans `restrictions.forbidden_actions` est recommandée : `"formuler_conseil_medical"`.
- **Code de la santé publique, article L.1111-2** : droit d'information du patient. L'agent ne se substitue pas à cette obligation, il ne fait que rediriger.

## Clients vulnérables — transversal

- **Code de la consommation, article L.121-21** : protection renforcée des consommateurs vulnérables. L'agent doit disposer d'un déclencheur de détresse et escalader immédiatement (`human_oversight.mandatory_escalation_triggers : client_manifeste_detresse`).
- **Charte de bonne conduite des conseillers numériques** (référentiel informel mais opposable en contentieux) : proscrire toute manipulation émotionnelle, toute urgence fabriquée, toute promotion commerciale auprès d'un client en difficulté manifeste.

## Secteur public et services essentiels

Si l'agent intervient pour le compte d'une personne publique ou d'un opérateur de services essentiels :

- **Directive (UE) 2022/2555 (NIS 2)** transposée par la loi n° 2024-364 : obligations de sécurité renforcées, notification d'incidents.
- **Code des relations entre le public et l'administration, article L.311-3-1** : obligation d'information sur l'usage d'un traitement algorithmique fondant une décision individuelle. Si l'agent intervient dans une décision administrative, l'article 50 de l'AI Act ne suffit pas — il faut aussi se conformer à cet article national.

## Points à valider par un juriste

- Confirmer le rattachement sectoriel du déploiement (un acteur e-commerce peut être aussi soumis à DORA s'il propose du paiement fractionné).
- Lister les régulateurs sectoriels à informer en cas d'incident (CNIL, Arcep, ACPR, DGCCRF, ANSSI selon les cas).
- Vérifier les obligations de transparence renforcée au-delà de l'article 50 de l'AI Act (secteur public notamment).
