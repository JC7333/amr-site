# amr-site

Site public d'AMR (Agent Mandate Registry) : https://www.mandatia.eu

- Code d'AMR (serveur MCP) : https://github.com/JC7333/amr
- Licence : Apache-2.0 (fichier LICENSE), comme le code d'AMR. Polices : SIL Open Font License 1.1 (assets/fonts).

## Modifier le site

Les pages `.html` de la racine et de `en/` sont **générées**. On ne les modifie jamais à la main.

1. Modifier la source dans `src/` (voir le tableau).
2. `python tools/build.py` régénère les pages.
3. `python tools/check.py` contrôle le résultat. `python tools/check.py --selftest` vérifie que les contrôles voient encore chaque défaut connu.
4. `python tools/serve.py` sert le site en local, avec les mêmes en-têtes de sécurité que la production.

Aucune dépendance : Python 3.9 ou plus récent suffit, sous Windows aussi.

| Pour changer | Modifier |
|---|---|
| un chiffre ou une date (tests, version, places pilotes, date de mise à jour) | `src/data/facts.json` |
| le texte d'une page | `src/pages/fr/…` et `src/pages/en/…` |
| une question fréquente | `src/data/faq.json` |
| un outil (la liste vient du code d'AMR) | `src/data/tools.json` |
| un gabarit | `src/data/gabarits.json` |
| le menu, le pied de page, les titres et descriptions des pages | `tools/build.py` (tables `PAGES` et `T`) |
| l'apparence | `assets/site.css` |
| la définition de « mandat » (une seule phrase, reprise partout) | `src/data/facts.json`, clés `def_mandat` et `def_mandat_en` |
| la démonstration (vraies réponses du registre, mandats signés par leur mandant, instantané signé) | `tools/make_demo_registry.py`, qui réécrit `assets/demo/` |
| les images d'aperçu des liens | `tools/og/`, à capturer en 1200 x 630 vers `assets/og-fr.jpg` et `assets/og-en.jpg` |

## Ce que le site tient, et que les contrôles vérifient

- Aucune ressource chez un tiers, aucun cookie, aucun style ni script en ligne (politique de sécurité dans `vercel.json`).
- Tout le contenu est lisible sans JavaScript. Seule la page « Vérifier » en a besoin, et elle le dit.
- Français à la racine, anglais sous `/en/`, une adresse par langue.
- La démonstration n'est pas simulée : `assets/demo/` est produit par le code d'AMR. Le mandat de démonstration dure un an ; le contrôle prévient 45 jours avant son expiration.
