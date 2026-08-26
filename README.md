# cv-checker — vérificateur de CV pour alternants IT

Un CV d'alternant se relit à la chaîne, et il y manque toujours les mêmes
choses : le téléphone, le rythme d'alternance, la disponibilité. Ce dépôt
automatise ce contrôle.

Le CV s'écrit en **Markdown** — versionnable, diffable, relisible en pull
request. Un script Python vérifie qu'il contient les informations minimum
attendues, et la CI regénère à chaque push une version **`.docx`** propre et
lisible par les ATS (les robots de tri des recruteurs).

## Ce qui est vérifié

| Champ | Attendu |
| --- | --- |
| Nom et prénom | Titre `# Prénom Nom` en tête de CV |
| Email | Adresse au format valide |
| Téléphone | Numéro français (`06 12 34 56 78`, `+33 6 12 34 56 78`, …) |
| Formation | Section `## Formation` non vide |
| Expérience | Section `## Expérience` non vide |
| Compétences | Section `## Compétences` non vide |
| Rythme d'alternance | 3 semaines en entreprise, 1 vendredi sur 3 à l'école, 33 h d'e-learning sur 3 semaines |
| Disponibilité | La formule « dès que possible » |

Cette liste vit dans **[`config.yml`](config.yml)**, pas dans le code : ajouter
ou assouplir un critère se fait en éditant ce fichier.

## Démarrage

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Partir du modèle
cp templates/cv-template.md data/mon-cv.md   # data/ est ignoré par git

# 2. Le remplir, puis le vérifier
python check_cv.py data/mon-cv.md
```

Sortie type sur un CV incomplet :

```
  [OK]      Nom et prénom        Camille Dubois
  [MANQUE]  Téléphone            introuvable ou format invalide
        -> Ajoute un numéro de téléphone français valide
           (formats acceptés : `06 12 34 56 78`, `+33 6 12 34 56 78`).

Résultat : 7/8 champs présents — à compléter : Téléphone.
```

### Options

```
python check_cv.py <cv.md> [-c config.yml] [-r rapport.md] [--no-color] [-q]
```

- `-c, --config` : autre fichier de champs attendus.
- `-r, --report` : écrit aussi le rapport dans un fichier
  (`.md` → tableau Markdown, sinon texte brut).
- `-q, --quiet` : n'affiche que la ligne de verdict.

Codes de sortie : **0** tout est présent · **1** il manque un champ requis ·
**2** erreur d'exécution (fichier ou config illisible).

### Export .docx

```bash
pandoc data/mon-cv.md --standalone -o dist/mon-cv.docx
```

La CI le fait automatiquement et publie le `.docx` en artefact téléchargeable
depuis l'onglet *Actions* de GitHub.

## Tests

```bash
pytest
```

La suite couvre un CV complet (le template, qui doit passer) et un CV incomplet
(qui doit échouer), la validation des formats, le parseur Markdown et les codes
de sortie de la CLI.

## Intégration continue

`.github/workflows/check-cv.yml` tourne à chaque **push** et chaque **pull
request** : vérification des champs, `pytest`, conversion pandoc, publication du
`.docx` et du rapport en artefacts. Une PR à laquelle il manque un champ minimum
passe au rouge.

## ⚠️ RGPD — aucun CV réel dans le dépôt

Un CV contient des données personnelles (nom, coordonnées, parcours). **Seuls le
template fictif `templates/cv-template.md` et les fixtures fictives de `tests/`
sont versionnés.** Les CV réels se travaillent dans `data/`, exclu par le
`.gitignore`, et ne doivent jamais être committés — ni dans une issue, ni dans un
message de commit, ni dans un artefact publié.

Si un CV réel se retrouve committé par erreur, il faut le retirer de
l'historique (pas seulement du dernier commit) et prévenir la personne
concernée.

## Organisation du dépôt

`sessions/` (mémoire entre sessions de travail), `todos/`, `tasks/` (specs de
lots de travail), `bugs/`. Les conventions de nommage et d'archivage sont
décrites dans [`CLAUDE.md`](CLAUDE.md).
