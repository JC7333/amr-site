# amr-site : règles de travail

Site public de mandatia.eu. Lire `README.md` d'abord : il dit quel fichier modifier pour quoi.

## Règles qui ne se discutent pas

1. **Ne jamais modifier à la main** un `.html` de la racine ou de `en/`, ni `sitemap.xml`, `robots.txt`, `llms.txt`. Modifier `src/`, puis `python tools/build.py`. Une demande de fusion contient toujours la source et les pages régénérées.
2. Avant toute demande de fusion : `python tools/build.py --check`, `python tools/check.py` et `python tools/check.py --selftest` passent tous les trois.
3. **Un chiffre, une source** : aucun nombre d'outils, de tests, de gabarits, aucune version ni date écrits en dur dans une page. Ils viennent de `src/data/facts.json` (`{{f:clé}}`) ou sont comptés par le générateur.
4. **Aucune ressource chez un tiers** : pas de police, script, image ou feuille de style servis par un autre site. Aucun style ni script en ligne (la politique de sécurité les bloque).
5. **Français et anglais ensemble** : toute page nouvelle ou modifiée l'est dans les deux langues, sauf les deux articles longs en français.
6. **Voix d'Audric** (skill amr-funnel) : pas de tiret long, pas de points de suspension typographiques, phrases de longueurs inégales, aucune formule de machine, « médecin » et jamais « thermaliste », jamais « startup ».
7. **Décisions d'Audric du 13/11/2026** : titre « Pas de mandat valide, pas d'action. » ; « mandat » est défini une fois comme l'autorisation écrite qu'une personne ou un organe donne pour son agent ; jamais « mandat légal », « autorité légale » ni l'article 1984 dans la vitrine ; programme pilote annoncé (5 organisations, santé et assurance d'abord, gratuit, tout par écrit, aucun délai promis).
8. **Règles du Cap AMR** : jamais « conforme » ni « opposable » ; aucun prix ; aucun nom ni citation d'un contact ; aucune promesse de délai ou de garantie ; dire ce qu'AMR ne fait pas.
9. **Demande de fusion en brouillon** si elle touche un texte de droit, les mentions légales, `vercel.json`, `.github`, `LICENSE` ou ce fichier. La fusion est le clic d'Audric.
10. Le site suit le code : quand un outil ou un gabarit change dans `JC7333/amr`, mettre à jour `src/data/tools.json` ou `src/data/gabarits.json`, et `facts.json` (version publiée, nombre de tests et leur date).

## Repères

- La démonstration (`assets/demo/`) vient de `tools/make_demo_registry.py`, lancé avec le vrai code d'AMR. Ne jamais écrire ces fichiers à la main, ne jamais mettre une clé privée dans le dépôt.
- Les articles repris (`pourquoi-autorisation-prospective`, `pour-compliance-officers`, `ia-agentique-droit-union`, `mentions-legales`) gardent leur texte d'origine. Les contrôles de tirets et de décisions ne s'y appliquent pas.
- Vérification visuelle : `python tools/serve.py`, puis regarder l'accueil en largeur de téléphone et d'ordinateur.
