# Guide de déploiement — Agent Marketing & Contenu

Ce guide accompagne la mise en production du mandat AMR pour un agent de production de contenu marketing. Il s'adresse à l'équipe qui opère le déploiement (marketing, juridique, IT, DPO).

## Avant de commencer — checklist de pré-requis

- [ ] Charte éditoriale et guide de marque à jour, accessibles à l'agent en lecture seule.
- [ ] Liste blanche des marques tierces autorisées (clients, partenaires, citations presse) validée par le juridique.
- [ ] Politique de confidentialité du site web mise à jour pour mentionner l'usage d'un agent IA dans le marketing (article 13 RGPD).
- [ ] DPO identifié et associé au projet, avec accord écrit sur le mandat.
- [ ] Responsable éditorial désigné et formé aux cas d'escalade.
- [ ] Outil de marketing automation et CMS audités : capacité à recevoir des brouillons, à tracer la décision humaine de publication, à conserver les journaux.

## Étape 1 — Renseigner les valeurs du gabarit

Ouvrir `mandate.yaml` et remplacer toutes les valeurs entre `< >` par les valeurs propres à l'organisation : raison sociale, SIREN, identité du représentant, identifiants de l'agent, version du modèle LLM, zone d'hébergement, dates de validité.

Pour les volumes (`max_volume_per_day`, `max_per_day`), partir des valeurs du profil équilibré (`examples/03-equilibre.yaml`) et ajuster à la baisse pour un premier déploiement. Il est plus simple d'augmenter un plafond après quelques semaines de retour terrain que de l'abaisser après un incident.

## Étape 2 — Choisir le profil

Sélectionner un des trois exemples :

- `examples/01-permissif.yaml` : équipe éditoriale mature, charte stricte, redacteur en chef dédié.
- `examples/02-restrictif.yaml` : secteur régulé (banque, assurance, santé) ou phase pilote.
- `examples/03-equilibre.yaml` : profil par défaut recommandé pour la majorité des ETI B2B.

Copier le contenu du profil choisi par-dessus les sections correspondantes de `mandate.yaml`. Conserver les sections `metadata`, `compliance_mapping` et `audit_trail` du gabarit principal.

## Étape 3 — Validation juridique

Soumettre le mandat complet :

1. Au **DPO** : valider la base légale RGPD, la durée de conservation, l'absence de bascule article 22.
2. Au **service juridique** : valider les exclusions propriété intellectuelle, la liste des marques autorisées, les claims réglementés selon le secteur.
3. Au **directeur marketing** : valider l'alignement avec la charte éditoriale et les volumes attendus.

Toute zone marquée **À VALIDER PAR JURISTE** dans les fichiers `compliance/` doit faire l'objet d'une décision documentée avant mise en production.

## Étape 4 — Intégration technique

- Charger `mandate.yaml` dans le registre AMR (Tier 1 ou auto-hébergé).
- Configurer l'agent pour qu'il appelle le registre AMR avant chaque action mentionnée dans `permissions.invoke`. Sans token mandate-gated, l'agent ne doit pas pouvoir soumettre, publier ni envoyer.
- Activer le marquage C2PA (ou équivalent) dans la chaîne de génération, conformément à `agent.output_marking`.
- Activer les journaux SHA-256 chaînés (`audit_trail.tamper_evidence`).
- Brancher le CMS et l'outil de marketing automation pour qu'aucune publication ne soit possible sans validation humaine traçable.

## Étape 5 — Formation

- Former le ou les **réviseurs** désignés (responsable éditorial, redacteur en chef) aux cinq sujets listés dans `human_oversight.reviewer_profile.training_topics` : limites de l'agent, droit d'auteur et droit des marques, RGPD prospection et profilage, AI Act articles 50 et 26, code de la consommation pratiques commerciales.
- Préparer un **kit d'incident** : qui contacter, comment révoquer le mandat, comment retirer un contenu publié à tort.

## Étape 6 — Mise en production progressive

Recommandation : trois phases.

1. **Pilote silencieux (2-4 semaines)** : l'agent produit, l'humain valide, mais aucune publication n'est faite à partir des sorties de l'agent. Objectif : mesurer la qualité, ajuster les seuils.
2. **Pilote ouvert (4-8 semaines)** : publication avec mention humaine visible systématique, échantillonnage 100 % par le réviseur. Objectif : valider l'alignement avec la charte.
3. **Production (sans limite, durée du mandat)** : passage à l'échantillonnage statistique, conformément au profil retenu. Suivi mensuel des indicateurs.

## Points d'attention critiques

- **Aucune publication directe** : même en profil permissif, le mandat impose `max_per_day: 0` pour `publier_post_social` et `envoyer_campagne_email`. Cette règle ne doit jamais être contournée.
- **Marquage** : l'article 50, paragraphe 4 de l'AI Act est applicable au **2 août 2026**. La chaîne de marquage doit être opérationnelle à cette date pour éviter le risque d'amende article 99, paragraphe 4.
- **Marques tierces** : la mention d'une marque concurrente, même bienveillante, sans autorisation écrite, expose à l'article L.713-2 du Code de la propriété intellectuelle. La liste blanche est le seul périmètre autorisé.
- **Données d'audience** : l'agent ne lit jamais de données nominatives. La personnalisation nominative est faite hors agent par l'outil d'envoi.

## Checklist finale avant mise en prod

- [ ] `mandate.yaml` validé par DPO, juridique, marketing.
- [ ] Profil choisi et appliqué.
- [ ] Liste blanche des marques tierces annexée.
- [ ] Charte éditoriale annexée.
- [ ] Marquage C2PA fonctionnel.
- [ ] Journaux SHA-256 chaînés actifs.
- [ ] Aucune action de publication ne peut s'exécuter sans token AMR valide.
- [ ] Réviseur formé.
- [ ] Procédure de révocation documentée et testée.
- [ ] Notice utilisateur (article 50.1) en place sur les canaux conversationnels publics.
- [ ] Politique de confidentialité mise à jour.
