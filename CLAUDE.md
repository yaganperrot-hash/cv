# CLAUDE.md — briefing de session

> Lis ce fichier en entier au démarrage, puis **`sessions/last-session/`** (où on
> en est) et **`todos/todos.md`** (ce qu'il reste à faire) avant de toucher au code.

## 1. Le projet en deux phrases

Vérificateur de CV pour des étudiants en alternance IT. Le CV est écrit en
**Markdown** (versionnable, diffable) ; un script Python vérifie qu'il contient
les informations minimum attendues, et une CI (GitHub Actions + GitLab CI)
rejoue ce contrôle à chaque push / pull request.

Le script sort en **code 0** si tout est présent, **1** s'il manque un champ
requis (la CI passe au rouge), **2** en cas d'erreur d'exécution.

Champs minimum vérifiés : nom/prénom, email (format validé), téléphone (format
validé), sections Formation / Expérience / Compétences, rythme d'alternance
(3 semaines en entreprise, 1 vendredi sur 3 à l'école, 33 h d'e-learning sur
3 semaines) et disponibilité (« dès que possible »).

## 2. Stack et conventions techniques

| Élément | Choix |
| --- | --- |
| Langage | Python 3.12+, bibliothèque standard + PyYAML |
| Tests | pytest (`pytest` à la racine, config dans `pyproject.toml`) |
| Config | `config.yml` — **source de vérité des champs attendus** |
| Format CV | Markdown, sections en titres `##` |
| CI | `.github/workflows/check-cv.yml` + `.gitlab-ci.yml` |
| Sujet | `tasks/TASK-003-sujet-pro-intg.md` — énoncé distribué aux étudiants |

Règles de code :

- **Aucun champ attendu codé en dur dans le Python.** Ajouter, retirer ou
  assouplir un critère = éditer `config.yml`. Le code ne connaît que des *types*
  de règles : `heading`, `section`, `regex`, `all_of`.
- Un nouveau *type* de règle se déclare dans `cv_checker/config.py` et
  s'implémente dans `cv_checker/checker.py` — et arrive avec ses tests.
- Français pour les messages destinés aux étudiants, les commentaires et les
  commits ; anglais pour les identifiants de code.
- Commentaires rares et utiles : expliquer le *pourquoi*, jamais le *quoi*.

Modules :

```
check_cv.py            lanceur CLI
cv_checker/config.py   lecture + validation de config.yml
cv_checker/document.py parseur Markdown (titres, sections)
cv_checker/checker.py  moteur de règles -> Report
cv_checker/report.py   rendu console + artefact .md/.txt/.json
cv_checker/text.py     normalisation (minuscules, accents)
```

## 3. Structure du dépôt et mode d'emploi

```
CLAUDE.md              ce briefing
README.md              doc pour les humains
config.yml             champs minimum attendus
check_cv.py            point d'entrée CLI
cv_checker/            le code du vérificateur
templates/             CV modèle (fictif) qui passe le check
tests/                 pytest + fixtures fictives (CV de test)
reports/               rapports de vérification des CV fictifs (versionnés)
data/                  CV réels, **ignoré par git** (RGPD)
sessions/              mémoire de travail entre sessions
todos/                 travail à faire
tasks/                 spécifications de lots de travail
bugs/                  bugs ouverts et résolus
.github/workflows/     CI GitHub Actions
.gitlab-ci.yml         CI GitLab
ci/                    scripts helpers pour la CI GitLab
```

### Où ranger quoi

| Tu veux noter… | Ça va dans… |
| --- | --- |
| L'état d'arrivée d'une session (résumé, décisions, prochaine étape) | `sessions/last-session/session.md` |
| Une session terminée qu'on veut garder | `sessions/archive/YYYY-MM-DD-titre.md` |
| Une chose à faire, courte, sans spec | `todos/todos.md` |
| Un lot de travail à spécifier avant de coder | `tasks/TASK-000-titre.md` |
| Un comportement cassé | `bugs/bugs.md` |
| Un bug réparé | `bugs/archive/YYYY-MM-DD-BUG-000-titre.md` |
| Un **CV de test fictif** | `tests/fixtures/cv-<cas>.md`, couvert par un test |
| Un **CV réel** d'étudiant | `data/`, ignoré par git — jamais committé |
| Le rapport d'un CV **fictif** | `reports/<nom-du-cv>-report.md` |
| Le rapport d'un CV **réel** | nulle part dans le dépôt : il contient ses coordonnées |

### Conventions de nommage

- Dates : **`YYYY-MM-DD`**, toujours (tri alphabétique = tri chronologique).
- Fichiers : `kebab-case`, sans accent ni espace.
- Identifiants : `TASK-001`, `BUG-001`, `TODO-001` — numérotation à 3 chiffres,
  **incrémentale et jamais réutilisée**, même après archivage.
- Archives : `YYYY-MM-DD-<id>-titre.md` (`2026-08-26-BUG-001-parse-accents.md`).
- Branches : `setup`, `feat/<sujet>`, `fix/BUG-001-<sujet>`, `docs/<sujet>`.
- Commits : `type(scope): résumé à l'impératif` — types `feat`, `fix`, `docs`,
  `test`, `ci`, `chore`, `refactor`. Un commit = un changement cohérent.

### Rituel de fin de session

1. Faire tourner `pytest` et le check sur le template : tout doit être vert.
   Régénérer `reports/` si `config.yml`, le template ou une fixture a bougé.
2. Mettre à jour `sessions/last-session/session.md` avec l'état **réel**
   (ce qui marche, ce qui ne marche pas, la prochaine étape).
3. Déplacer les todos terminées dans `todos/archive/YYYY-MM-DD-titre.md`,
   les bugs résolus dans `bugs/archive/`.
4. Avant d'écraser `sessions/last-session/`, copier la version précédente dans
   `sessions/archive/YYYY-MM-DD-titre.md`.

## 4. Règles de travail (non négociables)

1. **Brancher avant de coder.** Jamais de commit direct sur `main`.
   `git switch -c feat/<sujet>` d'abord. Pas de merge sans relecture humaine.
2. **Jamais de CV réel dans le dépôt (RGPD).** Un CV d'étudiant contient des
   données personnelles : nom, adresse, téléphone, parcours. Seuls sont
   versionnés le template fictif (`templates/cv-template.md`) et les fixtures
   fictives de `tests/`. Les CV réels vivent dans `data/`, ignoré par git.
   Si un CV réel a été committé par erreur : le retirer de l'historique, ne pas
   se contenter d'un commit de suppression, et prévenir la personne concernée.
   Aucun nom, email ou téléphone réel non plus dans un test, une issue ou un
   message de commit.
3. **Tests verts avant de committer** : `pytest` + `python check_cv.py
   templates/cv-template.md`. Une modification de `config.yml` qui casse le
   template casse la CI de tout le monde.
4. **Toute évolution des champs attendus passe par `config.yml`** et par un test
   qui la couvre.
   Un CV de test ajouté au dépôt est fictif, vit dans `tests/fixtures/` et
   arrive avec le test qui le couvre — sinon c'est un fichier mort.
5. Ce qui a été décidé se note (`sessions/`), ce qui reste à faire se note
   (`todos/`), ce qui est cassé se note (`bugs/`). Une session qui ne laisse pas
   de trace fait perdre du temps à la suivante.

## 5. Commandes utiles

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python check_cv.py templates/cv-template.md              # vérifie le template
python check_cv.py data/mon-cv.md --report reports/cv.md # vérifie + artefact
python check_cv.py data/                                  # vérifie un dossier
python check_cv.py templates/cv-template.md --json        # sortie JSON
pytest                                                    # suite de tests

# Régénérer les rapports versionnés des CV fictifs
for cv in templates/cv-template.md tests/fixtures/*.md; do
  python check_cv.py "$cv" --no-color --quiet \
    --report "reports/$(basename "${cv%.md}")-report.md"
done
```
