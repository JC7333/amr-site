# Règles sectorielles françaises — Recrutement

En complément de l'AI Act et du RGPD, le déploiement d'un agent IA en recrutement doit respecter le cadre du droit du travail français et les recommandations des autorités compétentes.

## Code du travail — Non-discrimination

### Article L.1132-1

Interdit toute discrimination directe ou indirecte dans l'embauche sur une liste de critères protégés (origine, sexe, âge, état de santé, handicap, opinions, appartenance syndicale, etc.).

Dans le template : section `restrictions.prohibited_criteria` liste les critères sur lesquels l'agent ne peut jamais fonder une recommandation. Cette liste est dérivée de L.1132-1 et de l'article 225-1 du Code pénal.

### Article 225-1 du Code pénal

Définit pénalement la discrimination. Une décision défavorable assistée par un agent qui utiliserait un critère prohibé exposerait l'organisation — et potentiellement les personnes physiques responsables — à des sanctions pénales.

## Code du travail — Transparence et pertinence

### Article L.1221-6

Les informations demandées au candidat ne peuvent avoir comme finalité que d'apprécier sa capacité à occuper l'emploi proposé ou ses aptitudes professionnelles. Elles doivent présenter un **lien direct et nécessaire** avec l'emploi ou les aptitudes professionnelles évaluées.

Dans le template : section `permissions.read.fields_allowed` et `fields_forbidden`.

### Article L.1221-8

Le candidat doit être **expressément informé**, préalablement à leur mise en œuvre, des méthodes et techniques d'aide au recrutement utilisées à son égard.

Implication directe : les candidats doivent être informés de l'existence et de la nature de l'agent IA avant que leur candidature soit traitée. Une simple mention dans la politique de confidentialité n'est probablement pas suffisante. **À VALIDER PAR JURISTE.**

### Article L.1221-9

Aucune information concernant personnellement un candidat ne peut être collectée par un dispositif qui n'a pas été porté préalablement à sa connaissance.

Implication : la configuration de l'agent (périmètre, critères évalués, modèle utilisé) doit être descriptible dans une notice communicable.

## Information des représentants du personnel

### Articles L.2312-38 et L.2312-26 du Code du travail

Le comité social et économique (CSE) est informé et consulté sur les questions intéressant l'organisation du travail et sur l'introduction de nouvelles technologies ayant un impact sur les conditions de travail ou l'emploi.

Le déploiement d'un agent de recrutement entre dans ce champ. Une consultation formelle est recommandée avant mise en production. **À VALIDER PAR JURISTE.**

## CNIL — Référentiels applicables

- **Délibération n° 2019-160 du 21 novembre 2019** portant adoption d'un référentiel relatif aux traitements de données à caractère personnel mis en œuvre aux fins de gestion des activités de ressources humaines.
- **Recommandations CNIL en matière de recrutement** : principe de pertinence, loyauté de la collecte, information préalable.
- **Guidance CNIL sur l'IA** (publications 2023-2025) : à suivre pour les mises à jour.

## Défenseur des droits

Le Défenseur des droits peut être saisi par un candidat qui s'estime discriminé. Il dispose de pouvoirs d'enquête et peut demander communication des pièces, y compris **le mandat et les journaux d'audit de l'agent**.

La traçabilité produite par AMR est directement utile dans ce cadre.

## Conventions collectives

Certaines conventions collectives contiennent des dispositions spécifiques sur le recrutement (procédures, priorité de reclassement, etc.). Le mandat doit être relu par le service juridique de l'organisation au regard de la ou des conventions applicables. **À VALIDER PAR JURISTE.**

## Accords collectifs internes

Un accord d'entreprise peut encadrer l'usage de l'IA au-delà des obligations légales. Vérifier l'existence d'un tel accord avant déploiement.

## Secteurs particuliers

### Secteur public

Les administrations publiques sont soumises à des obligations additionnelles : statut général de la fonction publique, principes d'égal accès aux emplois publics, obligations renforcées de motivation des décisions. Un template spécifique au secteur public est recommandé — **non couvert par ce template v1**.

### Secteur bancaire et assurance

Certains postes sont soumis à habilitation (ACPR, AMF). Le tri de candidatures pour ces postes doit respecter les exigences d'honorabilité et de compétence. **Hors périmètre de ce template.**

### Santé

Le recrutement de professionnels de santé implique des vérifications d'inscription aux ordres et d'autorisations d'exercice. **Un template dédié santé est prévu dans la feuille de route AMR.**
