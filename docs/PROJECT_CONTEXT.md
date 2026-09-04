# Contexte du projet — Güdlft / OC Projet 11

> Ce document sert de mémoire de référence pour toutes nos futures conversations sur ce projet. Il doit rester à jour au fil de l'avancement.

## 0. Comment travailler avec moi sur ce projet

- **Je suis étudiant.** Je suis là pour apprendre, mais je dois avancer **vite** — je n'ai pas beaucoup de temps à consacrer à ce projet.
- **Le PDF de spécifications fonctionnelles OC P11 est la source de vérité absolue.** C'est lui qui guide le projet et son bon déroulement, avant toute autre considération.
- **Le système de branches imposé ne doit jamais être négligé.** Toujours travailler dans la bonne branche (ex: branche `QA` pour la revue de Sam), jamais directement sur `master`/`main` sans raison validée.
- **Approche TDD (Test-Driven Development)** : on écrit les tests avant ou en parallèle immédiat du code, pas après.

## 1. Contexte métier (fictif — scénario OpenClassrooms)

**Güdlft** est une société qui a créé une plateforme numérique pour coordonner des compétitions de force (deadlifting, strongman) en Amérique du Nord et en Australie.

- À l'origine : compétitions pour clubs locaux.
- Aujourd'hui : la société a pivoté et n'accueille plus que des compétitions pour des **marques de vêtements de fitness**, laissant les clubs régionaux sans solution abordable.
- Suite à des critiques sur les réseaux sociaux (clubs régionaux mécontents de ne plus être soutenus), Güdlft crée une équipe **Regional Outreach**.
- Objectif de cette équipe : construire une version **plus légère et moins coûteuse** de la plateforme, dédiée aux organisateurs régionaux, pour rationaliser la gestion des compétitions entre clubs (hébergement, inscriptions, frais, admin).

## 2. Ma mission

Sam Osei (développeur principal) a livré la **Phase 1** du prototype, puis s'est absenté (imprévu familial). Je reprends le projet :

1. **Corriger les bugs de la Phase 1** signalés par la QA (dont un bug qui **crashe l'application**).
2. **Implémenter les fonctionnalités de la Phase 2** (listées dans les issues du repo).
3. **Livrables attendus** :
   - Un **rapport de tests** (happy paths **et** sad paths, couverture complète des fonctionnalités).
   - Un **rapport de performances** (via Locust).
   - Le tout conforme au guide de développement en fin des spécifications fonctionnelles (le PDF — voir section 0).
4. Livraison sur une **branche QA** dédiée, revue ensuite par l'équipe sur : résolution des bugs, conformité aux rapports/normes, qualité du code, couverture de tests des nouvelles fonctionnalités.

## 3. Stack technique

- **Python 3** + **Flask** (pas de Django — volontairement minimal)
- **Pas de base de données** : persistance via fichiers **JSON** (`clubs.json`, `competitions.json`)
- **pytest** — framework de tests
- **Locust** — tests de performance/charge
- **coverage** — mesure de la couverture de tests (demandé explicitmeent dans le README)
- Environnement virtuel dans `env/` (convention adoptée ici ; le README d'origine suggérait `virtualenv .` à la racine, mais on préfère isoler dans un sous-dossier `env/`, ignoré par `.gitignore`)

### Dépendances de base (`requirements.txt`)
```
click==7.1.2
Flask==1.1.2
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
Werkzeug==1.0.1
```
(pytest, coverage et locust sont à ajouter manuellement, non listés dans le fichier d'origine)

## 4. Structure du projet

```
Python_Testing/
├── server.py              # App Flask principale (routes)
├── clubs.json             # Données des clubs (nom, email, points)
├── competitions.json      # Données des compétitions (nom, date, places dispo)
├── requirements.txt
├── pytest.ini             # pythonpath=. pour que `pytest` seul trouve `server.py`
├── README.md
├── docs/                  # Documentation du projet (ce dossier)
│   ├── PROJECT_CONTEXT.md
│   ├── Spé_fonctionnel_OC_P11.pdf
│   └── issues_gudlft.csv
├── templates/
│   ├── index.html         # Page de connexion (saisie email)
│   ├── welcome.html       # Résumé après connexion (liste compétitions)
│   └── booking.html       # Page de réservation de places
├── tests/
│   ├── conftest.py        # Fixture `client` partagée (recharge clubs/competitions)
│   ├── unit/               # Tests unitaires (fonctions isolées, sans Flask/HTTP)
│   ├── integration/        # Tests d'intégration (plusieurs composants ensemble)
│   └── functional/         # Tests fonctionnels (via test_client, bout en bout)
│       └── test_show_summary.py
└── env/                   # Environnement virtuel (ignoré par git)
```

## 5. Modèle de données

### `clubs.json`
```json
{"clubs":[
    {"name":"Simply Lift", "email":"john@simplylift.co", "points":"13"},
    {"name":"Iron Temple", "email":"admin@irontemple.com", "points":"4"},
    {"name":"She Lifts", "email":"kate@shelifts.co.uk", "points":"12"}
]}
```
⚠️ `points` est stocké en **string**, pas en nombre — point d'attention pour les bugs de points (#2, #6).

### `competitions.json`
```json
{"competitions": [
    {"name":"Spring Festival", "date":"2020-03-27 10:00:00", "numberOfPlaces":"25"},
    {"name":"Fall Classic", "date":"2020-10-22 13:30:00", "numberOfPlaces":"13"}
]}
```
⚠️ Les deux dates sont dans le **passé** par rapport à aujourd'hui (03/09/2026) — utile pour tester l'issue #5 (réservation sur compétition passée) sans avoir à modifier les données de test.
⚠️ `numberOfPlaces` est aussi en **string**.

## 6. Routes actuelles de `server.py`

| Route | Méthode | Rôle | Lien avec les issues |
|---|---|---|---|
| `/` | GET | Page d'accueil / login (email) | — |
| `/showSummary` | POST | Cherche le club par email, affiche le résumé | **#1** : si l'email n'existe pas, `[club for ... ][0]` lève une `IndexError` → **crash** |
| `/book/<competition>/<club>` | GET | Affiche la page de réservation | — |
| `/purchasePlaces` | POST | Déduit les places réservées de la compétition | **#4, #5, #282** : aucune validation (places max, compétition passée, places disponibles) ; **#6** : ne déduit jamais les points du club |
| `/logout` | GET | Redirige vers l'accueil | — |
| *(TODO dans le code, ligne 54)* | — | Route pour afficher les points — **non implémentée** | **#7** |

## 7. Configuration Git

- **`origin`** → mon repo perso : `https://github.com/Volgar3/OC_P11.git`
- **`upstream`** → repo original OpenClassrooms : `https://github.com/OpenClassrooms-Student-Center/Python_Testing.git`
- Le repo original contient **beaucoup de bruit** (issues créées par d'autres apprenants sur le même repo partagé) — voir tableau des issues ci-dessous, qui liste tout sans filtrage.

## 8. Suivi des issues

Voir tableau détaillé et à jour dans [`issues_gudlft.csv`](./issues_gudlft.csv) (colonnes : Numero, Titre, Lien, Etat, Type, Description — importable tel quel dans Notion).

### Tableau de suivi (statuts au 03/09/2026)

| # | État GitHub | Type | Titre | Phase | Statut de traitement |
|---|---|---|---|---|---|
| [1](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/1) | open | 🔴 Bug critique | Un email inconnu crashe l'app | Phase 1 | ⬜ À faire |
| [2](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/2) | open | 🐛 Bug | Un club peut dépenser plus de points qu'il n'en a | Phase 1 | ⬜ À faire |
| [3](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/3) | closed | 🐛 Bug (doublon) | Réservation > 12 places/compétition — remplacée par #4 | — | ℹ️ Info seulement |
| [4](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/4) | open | 🐛 Bug | Réservation > 12 places/compétition (+ déduction du nb de places) | Phase 1 | ⬜ À faire |
| [5](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/5) | open | 🐛 Bug | Réservation possible sur une compétition passée | Phase 1 | ⬜ À faire |
| [6](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/6) | open | 🐛 Bug | Les points ne sont pas déduits après réservation | Phase 1 | ⬜ À faire |
| [7](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/7) | open | ✨ Feature | Tableau d'affichage des points par club | Phase 2 | ⬜ À faire |
| [38](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/38) | closed | ⚠️ Vide | "erreur à supprimer" — sans contenu | — | ℹ️ Ignorer |
| [132](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/132) | closed | 🐛 Note | Renvoie vers #4 | — | ℹ️ Info seulement |
| [269](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/269) | closed | ✨ Note | Renvoie vers #7 | — | ℹ️ Info seulement |
| [282](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/282) | open | 🐛 Bug | Réservation > places disponibles pour la compétition (stock global) | Phase 1 | ⬜ À faire |

**Légende statut de traitement** : ⬜ À faire · 🟨 En cours · ✅ Fait & testé · ❌ Bloqué

> ➡️ Mettre à jour la colonne "Statut de traitement" au fil de l'avancement, dans cette conversation ou directement dans ce fichier.

## 9. Guide de développement (extrait fidèle du PDF de spécifications fonctionnelles, p.4-5)

> ⚠️ Cette section retranscrit fidèlement le PDF `Spé_fonctionnel_OC_P11.pdf`. En cas de doute, le PDF reste la source de vérité absolue — ce résumé n'est qu'un aide-mémoire.

### Convention de nommage des branches
Format obligatoire : **`<fonctionnalité|bug|amélioration>/nom-descriptif`**
Exemple donné par le PDF : un bug trouvé → branche `bug/nom-de-bogue`.

### Règles de branches
- **`master`** = source de vérité (code fini, toujours fonctionnel). Tout le monde doit pouvoir cloner `master` et faire tourner le projet sans erreur.
- Toute fonctionnalité, bug ou amélioration → **sa propre branche**, créée depuis `master`.
- **Un seul sujet par branche** — jamais mélanger plusieurs bugs/features dans la même branche.
- On ne revient dans `master` (merge) **que lorsque tous les tests passent**. Si ça ne marche pas, ça n'a pas sa place dans `master`.
- Quand le code est prêt pour la revue : créer une **branche QA** depuis `master`. **Cette branche QA n'est JAMAIS fusionnée dans master** — elle sert uniquement à la revue.

### Tests
- Toujours tester : *"Si vous ne l'avez pas testé, il est cassé."*
- Framework libre (pytest, unittest, Morelia...) mais lançable en ligne de commande — **on utilise pytest**.
- **Tous les tests dans un dossier `tests/`**, avec des **sous-dossiers séparés par type** : unitaires / intégration / fonctionnels.
  → Structure adoptée : `tests/unit/`, `tests/integration/`, `tests/functional/` (+ `tests/conftest.py` partagé).
- Priorité : **tests unitaires >> tests d'intégration >> tests fonctionnels**. Au minimum, écrire des tests unitaires.
- Cible : **au moins 2x plus de tests unitaires** que de tests d'intégration/fonctionnels cumulés.
- **Couverture minimale visée : 60%** du code.

### Performance
- Utiliser **Locust**.
- Temps de chargement d'une liste de compétitions : **jamais plus de 5 secondes**.
- Mise à jour du total de points : **jamais plus de 2 secondes**.
- **6 utilisateurs simulés par défaut** pour les tests de performance.

## 10. Rappel des specs fonctionnelles (Phase 0/1/2, PDF p.2-3)

- **Le pourquoi** : version allégée de la plateforme pour organisateurs locaux/régionaux, permettant aux clubs d'inscrire leurs athlètes.
- **Le comment** : seuls les **secrétaires de club** ont accès à l'app (pas les athlètes directement). Ils réservent des places avec les **points** du club (1 point = 1 inscription). Max **12 athlètes par club et par compétition**.
- **Phase 1** (déjà en place, bugs à corriger) : connexion par email, liste des compétitions à venir, achat de places avec points, message de confirmation ou d'erreur (concours complet), déduction des points du total, blocage si > places dispo ou > 12 places, déconnexion.
- **Phase 2** (à implémenter) : tableau **public** (sans connexion requise) des points de tous les clubs, en lecture seule.

## 11. Historique des décisions prises ensemble

- Venv placé dans `env/` (pas à la racine) — convention demandée explicitement, contrairement au README d'origine (`virtualenv .`).
- `.gitignore` restauré à partir de l'historique upstream, adapté : `bin/include/lib` remplacés par `env/`, et `tests/` retiré de l'ignore (on **doit** committer nos tests, contrairement au projet d'origine qui les ignorait).
- Remote `origin` repointé vers le fork perso (`OC_P11`), `upstream` conservé vers le repo OpenClassrooms d'origine — jamais de push accidentel vers le repo original.
