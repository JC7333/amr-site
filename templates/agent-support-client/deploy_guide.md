# Guide de déploiement — Agent Support Client

## Ordre de mise en production

1. **Cadrage avec le métier** : choisir le profil (permissif, restrictif, équilibré) en fonction du secteur et de la maturité. En première itération, choisir le profil restrictif ou équilibré. Le profil permissif se déverrouille après un retour d'expérience documenté.
2. **Renseignement du `mandate.yaml`** : remplacer toutes les valeurs entre `< >` par les données réelles de l'organisation (SIREN, représentant, agent, plafonds, canaux de disclosure).
3. **Revue DPO et juridique** : validation des points marqués « À VALIDER PAR JURISTE » dans les trois fiches de conformité, vérification que la base légale RGPD choisie est adaptée au cas d'usage, vérification des durées de conservation sectorielles.
4. **Chargement dans le registre AMR** : import du mandat dans le runtime Tier 1. Le token d'exécution de l'agent ne sera émis que si le mandat est valide, signé et non expiré.
5. **Intégration au canal client** : insertion de la notice de transparence article 50 en ouverture de conversation (chat web, email automatique, messagerie instantanée). La notice doit être journalisée à chaque affichage.
6. **Formation des équipes niveau 2** : sur les cas d'escalade, la reprise de conversation, la reconnaissance de détresse, le traitement d'une demande RGPD.
7. **Mise en production en mode pilote** : `human_in_the_loop` pendant au minimum 4 semaines, avec revue humaine systématique des réponses sortantes. Bascule vers `human_on_the_loop` sur décision formelle du comité.
8. **Revue périodique** : trimestrielle a minima, avec examen des journaux, des incidents, des réclamations, et ajustement des plafonds si nécessaire.

## Points d'attention critiques

- **La notice de transparence doit être visible, pas dissimulée.** Elle s'affiche au début de la conversation, pas dans un lien en pied de page. Un manquement sur ce point expose à l'article 99, paragraphe 4 du Règlement (UE) 2024/1689 : jusqu'à 15 M€ ou 3 % du chiffre d'affaires mondial.
- **Les plafonds financiers doivent être cohérents avec les délégations de signature internes.** Un agent ne peut pas avoir plus d'autonomie financière qu'un conseiller humain de même niveau.
- **L'agent ne doit pas nier être une IA si on le lui demande.** Cette règle est explicitée dans `restrictions.prohibited_behaviours`. Un défaut sur ce point cumule une sanction AI Act article 50 et une sanction au titre du Code de la consommation article L.121-2 (pratique commerciale trompeuse).
- **Aucune donnée bancaire en clair ne doit transiter par l'agent.** Interdit par `permissions.read.fields_forbidden`. La modification de ces données passe par un canal séparé et authentifié.
- **Toute montée en volume déclenche une réévaluation de la DPIA.** La DPIA n'est pas obligatoire a priori sur le périmètre du gabarit, mais un passage à 10 000 conversations par jour avec profiling peut suffire à basculer sous l'article 35 du RGPD.
- **L'expiration du mandat doit être surveillée.** Le runtime AMR Tier 1 refuse d'émettre un token pour un mandat expiré. Prévoir une alerte à J-30 pour relancer le processus de renouvellement.

## Checklist de validation avant mise en prod

- [ ] `mandate.yaml` rempli, sans aucune valeur entre `< >` restante.
- [ ] Signature du mandat par le représentant habilité (méthode eIDAS avancée ou qualifiée recommandée pour les secteurs régulés).
- [ ] Revue DPO signée.
- [ ] Revue juridique signée, avec décision explicite sur la nécessité d'une DPIA.
- [ ] Notice de transparence article 50 intégrée dans tous les canaux listés (`agent.user_disclosure.disclosure_channels`).
- [ ] Politique de confidentialité mise à jour et publiée.
- [ ] Formation niveau 2 réalisée, liste des personnes formées annexée.
- [ ] Période de pilote `human_in_the_loop` planifiée sur au moins 4 semaines.
- [ ] Plan de revue trimestrielle formalisé (qui, quand, quoi).
- [ ] Procédure de révocation d'urgence testée (un exercice au moins avant mise en prod).
- [ ] Journal d'audit connecté à un stockage non modifiable avec chaîne SHA-256 active.
- [ ] Numéro et adresse du DPO accessibles depuis la conversation à la demande du client.
